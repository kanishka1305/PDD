import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Download, FileDown, Share2, ChevronRight, AlertCircle, BarChart2, Cpu, Layers, Activity, TrendingUp } from 'lucide-react'
import AppLayout from '@/components/layout/AppLayout'
import { store, AnalysisResult } from '@/lib/store'
import { getStlUrl, getDicomUrl, getSegImgUrl } from '@/lib/api'
import { cn, fmtNumber } from '@/lib/utils'

const REGIONS = [
  { key: 'condylar_head_l_volume',          label: 'Condylar Head — Left',       color: '#3b82f6', colorClass: 'text-brand',   region: 'condylar_head_L',           zone: 'Superior' },
  { key: 'condylar_head_r_volume',          label: 'Condylar Head — Right',      color: '#60a5fa', colorClass: 'text-blue-400', region: 'condylar_head_R',           zone: 'Superior' },
  { key: 'coronoid_l_volume',               label: 'Coronoid Process — Left',    color: '#06b6d4', colorClass: 'text-cyan',     region: 'coronoid_L',                zone: 'Superior' },
  { key: 'coronoid_r_volume',               label: 'Coronoid Process — Right',   color: '#22d3ee', colorClass: 'text-cyan-300', region: 'coronoid_R',                zone: 'Superior' },
  { key: 'angle_ramus_l_volume',            label: 'Angle & Ramus — Left',       color: '#8b5cf6', colorClass: 'text-violet',   region: 'angle_ramus_L',             zone: 'Mid' },
  { key: 'angle_ramus_r_volume',            label: 'Angle & Ramus — Right',      color: '#a78bfa', colorClass: 'text-violet-300', region: 'angle_ramus_R',           zone: 'Mid' },
  { key: 'body_l_volume',                   label: 'Body — Left',                color: '#f59e0b', colorClass: 'text-amber',    region: 'body_L',                    zone: 'Inferior' },
  { key: 'body_r_volume',                   label: 'Body — Right',               color: '#fbbf24', colorClass: 'text-amber-300',region: 'body_R',                    zone: 'Inferior' },
  { key: 'symphyseal_parasymphyseal_volume',label: 'Symphyseal & Parasymphyseal',color: '#10b981', colorClass: 'text-emerald',  region: 'symphyseal_parasymphyseal', zone: 'Inferior' },
]

function RegionCard({ r, a, scanId }: { r: typeof REGIONS[0]; a: AnalysisResult['analysis']; scanId: number }) {
  const vol = (a as any)[r.key] as number
  const isEmpty = !vol || vol < 1

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
      className="card-hover p-4 flex flex-col gap-3" style={{ borderColor: `${r.color}22` }}>
      <div className="flex items-start justify-between">
        <div>
          <div className="text-[11px] font-semibold text-slate-500 uppercase tracking-wide mb-1">{r.zone}</div>
          <div className="text-sm font-semibold text-slate-100">{r.label}</div>
        </div>
        <div className="w-2 h-2 rounded-full mt-1 shrink-0" style={{ background: r.color }} />
      </div>
      {isEmpty ? (
        <div className="text-sm text-slate-500 italic">Not segmented</div>
      ) : (
        <div>
          <div className={cn('text-2xl font-bold font-mono', r.colorClass)}>{fmtNumber(vol)}</div>
          <div className="text-[11px] text-slate-500 mt-0.5">voxels</div>
        </div>
      )}
      <div className="flex gap-2 mt-auto">
        <a href={getStlUrl(scanId, r.region)} target="_blank" rel="noreferrer"
          className={cn('flex-1 btn btn-secondary text-xs justify-center py-1.5', isEmpty && 'opacity-40 pointer-events-none')}>
          <Download size={12} /> STL
        </a>
        <a href={getDicomUrl(scanId, r.region)} target="_blank" rel="noreferrer"
          className={cn('flex-1 btn btn-secondary text-xs justify-center py-1.5', isEmpty && 'opacity-40 pointer-events-none')}>
          <FileDown size={12} /> DCM
        </a>
      </div>
    </motion.div>
  )
}

export default function ResultsPage() {
  const navigate = useNavigate()
  const result = store.getResult()
  const a = result?.analysis
  const scanId = result?.scan_id ?? 0

  if (!result || !a) {
    return (
      <AppLayout breadcrumb={['DentAI', 'Results']} title="Results">
        <div className="flex flex-col items-center justify-center h-96 gap-4">
          <div className="w-16 h-16 rounded-2xl bg-navy-700 flex items-center justify-center">
            <AlertCircle size={28} className="text-slate-500" />
          </div>
          <div className="text-center">
            <h3 className="font-semibold text-white">No Results Available</h3>
            <p className="text-slate-400 text-sm mt-1">Upload and analyse a CBCT scan to see results here.</p>
          </div>
          <button onClick={() => navigate('/upload')} className="btn-primary">Upload Scan</button>
        </div>
      </AppLayout>
    )
  }

  const zones = ['Superior', 'Mid', 'Inferior']

  return (
    <AppLayout breadcrumb={['DentAI', 'Results', a.report_id]} title="Analysis Results" scanId={scanId}>
      <div className="space-y-6 animate-fade-in">
        {/* Header */}
        <div className="flex items-start justify-between flex-wrap gap-4">
          <div>
            <h1 className="text-xl font-bold text-white">Segmentation Results</h1>
            <p className="text-slate-400 text-sm mt-0.5">{a.report_id} · {a.report_date} · Scan #{scanId}</p>
          </div>
          <div className="flex gap-2 flex-wrap">
            <a href={getStlUrl(scanId, 'full')} target="_blank" rel="noreferrer" className="btn-secondary text-xs"><Download size={13}/> Full STL</a>
            <a href={getDicomUrl(scanId, 'full')} target="_blank" rel="noreferrer" className="btn-secondary text-xs"><FileDown size={13}/> Full DICOM</a>
            <button className="btn-secondary text-xs"><Share2 size={13}/> Share</button>
          </div>
        </div>

        {/* Summary stats */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { icon: Layers,    label: 'Total Bone Volume',  val: `${fmtNumber(a.bone_volume)} vox`, color: 'text-brand'   },
            { icon: Activity,  label: 'Cortical Bone',      val: `${fmtNumber(a.cortical_bone)} vox`, color: 'text-cyan'  },
            { icon: TrendingUp, label: 'Trabecular Bone',   val: `${fmtNumber(a.trabecular_bone)} vox`, color: 'text-violet' },
            { icon: Cpu,       label: 'AI Confidence',      val: `${a.confidence?.toFixed(1)}%`, color: 'text-emerald' },
          ].map(({ icon: Icon, label, val, color }) => (
            <div key={label} className="stat-card">
              <Icon size={18} className={cn('mb-2', color)} />
              <div className="text-lg font-bold text-white font-mono">{val}</div>
              <div className="text-xs text-slate-400">{label}</div>
            </div>
          ))}
        </div>

        {/* Clinical metrics */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div className="card p-5">
            <div className="section-header">Clinical Metrics</div>
            <div className="space-y-3">
              {[
                { label: 'Nerve Canal Volume',  val: `${a.nerve_canal_volume?.toFixed(2)} cm³` },
                { label: 'Nerve Distance',      val: `${a.nerve_distance_value?.toFixed(1)} mm`, badge: a.nerve_distance },
                { label: 'Bone Loss',           val: `${a.bone_loss?.toFixed(1)}%` },
                { label: 'Detected Voxels',     val: fmtNumber(a.detected_voxels).toString() },
                { label: 'Volume Shape',        val: a.volume_shape?.join(' × ') || '—' },
              ].map(({ label, val, badge }) => (
                <div key={label} className="flex items-center justify-between py-2 border-b border-navy-600 last:border-0">
                  <span className="text-sm text-slate-400">{label}</span>
                  <div className="flex items-center gap-2">
                    {badge && <span className={cn('badge text-[10px]', badge === 'HIGH' ? 'badge-red' : 'badge-green')}>{badge}</span>}
                    <span className="text-sm font-medium text-slate-200 font-mono">{val}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="card p-5">
            <div className="section-header">Segmentation Preview</div>
            {a.segmentation_image ? (
              <img src={getSegImgUrl(a.segmentation_image)} alt="Segmentation" className="w-full rounded-lg border border-navy-500 object-contain max-h-56" />
            ) : (
              <div className="h-48 flex items-center justify-center bg-navy-800 rounded-lg text-slate-500 text-sm">
                <BarChart2 size={24} className="mr-2 opacity-40" /> No preview available
              </div>
            )}
            <p className="text-[11px] text-slate-500 mt-2">Middle axial slice of the full mandible segmentation mask</p>
          </div>
        </div>

        {/* 7 Region cards by zone */}
        {zones.map(zone => {
          const zoneRegions = REGIONS.filter(r => r.zone === zone)
          return (
            <div key={zone}>
              <div className="flex items-center gap-3 mb-3">
                <div className="section-header mb-0">🦷 {zone} Zone</div>
                <div className="flex-1 h-px bg-navy-600" />
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-3">
                {zoneRegions.map(r => <RegionCard key={r.key} r={r} a={a} scanId={scanId} />)}
              </div>
            </div>
          )
        })}
      </div>
    </AppLayout>
  )
}
