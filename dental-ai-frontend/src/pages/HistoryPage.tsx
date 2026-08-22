import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { Search, Filter, ScanLine, Download, Play, RefreshCw, ChevronLeft, ChevronRight } from 'lucide-react'
import AppLayout from '@/components/layout/AppLayout'
import { getScans, analyzeScan } from '@/lib/api'
import { store } from '@/lib/store'
import { cn, fmtDate } from '@/lib/utils'

const PAGE_SIZE = 8

export default function HistoryPage() {
  const navigate = useNavigate()
  const [scans, setScans] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('all')
  const [page, setPage] = useState(0)
  const [analysing, setAnalysing] = useState<number | null>(null)

  useEffect(() => {
    getScans().then(r => setScans(r.data.scans || [])).catch(() => {}).finally(() => setLoading(false))
  }, [])

  const filtered = scans.filter(s => {
    const q = search.toLowerCase()
    const matchSearch = !q || s.patient_name?.toLowerCase().includes(q) || s.filename?.toLowerCase().includes(q) || String(s.id).includes(q)
    const matchStatus = statusFilter === 'all' || s.status === statusFilter
    return matchSearch && matchStatus
  })

  const totalPages = Math.ceil(filtered.length / PAGE_SIZE)
  const paged = filtered.slice(page * PAGE_SIZE, (page + 1) * PAGE_SIZE)

  const runAnalysis = async (scanId: number) => {
    setAnalysing(scanId)
    try {
      const { data } = await analyzeScan(scanId)
      store.setResult(data)
      navigate('/results')
    } catch (e) {
      alert('Analysis failed')
    } finally {
      setAnalysing(null)
    }
  }

  return (
    <AppLayout breadcrumb={['DentAI', 'History']} title="Scan History">
      <div className="space-y-5 animate-fade-in">
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <h1 className="text-xl font-bold text-white">Scan History</h1>
            <p className="text-slate-400 text-sm mt-0.5">{scans.length} total scans in database</p>
          </div>
          <button onClick={() => { setLoading(true); getScans().then(r => setScans(r.data.scans || [])).finally(() => setLoading(false)) }}
            className="btn-secondary text-xs"><RefreshCw size={13} /> Refresh</button>
        </div>

        {/* Search + filter */}
        <div className="flex items-center gap-3 flex-wrap">
          <div className="relative flex-1 min-w-[200px]">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input className="input pl-9 text-sm" placeholder="Search patient, filename, scan ID..." value={search} onChange={e => { setSearch(e.target.value); setPage(0) }} />
          </div>
          <select value={statusFilter} onChange={e => { setStatusFilter(e.target.value); setPage(0) }}
            className="input w-auto text-sm pr-8 cursor-pointer">
            <option value="all">All Status</option>
            <option value="uploaded">Uploaded</option>
            <option value="analysed">Analysed</option>
          </select>
        </div>

        {/* Table */}
        <div className="card overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-navy-500">
                  {['ID', 'Patient Name', 'Filename', 'Modality', 'Status', 'Date', 'Actions'].map(h => (
                    <th key={h} className="text-left text-[11px] font-semibold text-slate-500 uppercase tracking-wide px-4 py-3">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {loading ? (
                  Array.from({ length: 5 }).map((_, i) => (
                    <tr key={i} className="border-b border-navy-600">
                      {Array.from({ length: 7 }).map((_, j) => (
                        <td key={j} className="px-4 py-3"><div className="h-4 bg-navy-600 rounded animate-pulse w-3/4" /></td>
                      ))}
                    </tr>
                  ))
                ) : paged.length === 0 ? (
                  <tr><td colSpan={7} className="px-4 py-12 text-center text-slate-500">
                    <ScanLine size={28} className="mx-auto mb-2 opacity-40" />
                    {search ? 'No scans match your search.' : 'No scans uploaded yet.'}
                  </td></tr>
                ) : paged.map((s: any) => (
                  <motion.tr key={s.id} initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                    className="border-b border-navy-600 hover:bg-navy-700/50 transition-colors">
                    <td className="px-4 py-3 font-mono text-xs text-slate-400">#{s.id}</td>
                    <td className="px-4 py-3 font-medium text-slate-200">{s.patient_name || <span className="text-slate-500 italic">Unknown</span>}</td>
                    <td className="px-4 py-3 text-slate-400 font-mono text-xs max-w-[140px] truncate">{s.filename}</td>
                    <td className="px-4 py-3"><span className="badge-cyan">{s.modality || 'CT'}</span></td>
                    <td className="px-4 py-3"><span className={cn('badge text-[10px]', s.status === 'uploaded' ? 'badge-blue' : 'badge-green')}>{s.status}</span></td>
                    <td className="px-4 py-3 text-slate-400 text-xs">{fmtDate(s.created_at)}</td>
                    <td className="px-4 py-3">
                      <div className="flex items-center gap-2">
                        <button onClick={() => runAnalysis(s.id)} disabled={analysing === s.id}
                          className={cn('btn-secondary text-xs py-1 px-2.5', analysing === s.id && 'opacity-60')}>
                          {analysing === s.id ? <><RefreshCw size={11} className="animate-spin" /> Running...</> : <><Play size={11} /> Analyse</>}
                        </button>
                      </div>
                    </td>
                  </motion.tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Pagination */}
          {totalPages > 1 && (
            <div className="flex items-center justify-between px-4 py-3 border-t border-navy-500">
              <span className="text-xs text-slate-500">{filtered.length} records · Page {page + 1} of {totalPages}</span>
              <div className="flex items-center gap-1">
                <button onClick={() => setPage(p => Math.max(0, p - 1))} disabled={page === 0} className="btn-ghost p-1.5 disabled:opacity-40"><ChevronLeft size={14} /></button>
                {Array.from({ length: Math.min(totalPages, 5) }).map((_, i) => (
                  <button key={i} onClick={() => setPage(i)} className={cn('w-7 h-7 rounded text-xs', page === i ? 'bg-brand text-white' : 'btn-ghost')}>{i + 1}</button>
                ))}
                <button onClick={() => setPage(p => Math.min(totalPages - 1, p + 1))} disabled={page >= totalPages - 1} className="btn-ghost p-1.5 disabled:opacity-40"><ChevronRight size={14} /></button>
              </div>
            </div>
          )}
        </div>
      </div>
    </AppLayout>
  )
}
