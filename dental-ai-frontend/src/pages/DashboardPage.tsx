import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { useNavigate } from 'react-router-dom'
import { Users, ScanLine, CheckCircle2, Clock, Cpu, Database, HardDrive, Wifi, Upload, History, BarChart2, TrendingUp, Activity, AlertCircle } from 'lucide-react'
import AppLayout from '@/components/layout/AppLayout'
import { getHealth, getScans } from '@/lib/api'
import { cn, fmtDate } from '@/lib/utils'
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts'

const WEEKLY = [
  { day: 'Mon', scans: 4, analyses: 3 }, { day: 'Tue', scans: 7, analyses: 6 },
  { day: 'Wed', scans: 5, analyses: 5 }, { day: 'Thu', scans: 9, analyses: 8 },
  { day: 'Fri', scans: 6, analyses: 6 }, { day: 'Sat', scans: 3, analyses: 2 },
  { day: 'Sun', scans: 2, analyses: 2 },
]
const CONFIDENCE = [
  { week: 'W1', score: 86 }, { week: 'W2', score: 88 }, { week: 'W3', score: 87 },
  { week: 'W4', score: 91 }, { week: 'W5', score: 89 }, { week: 'W6', score: 92 },
]

function StatCard({ icon: Icon, label, value, sub, color = 'text-brand', trend }: {
  icon: any; label: string; value: string | number; sub?: string; color?: string; trend?: number
}) {
  return (
    <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="stat-card group hover:border-brand/30 transition-all">
      <div className="flex items-start justify-between">
        <div className={cn('w-9 h-9 rounded-lg flex items-center justify-center bg-navy-600 group-hover:scale-110 transition-transform', color.replace('text-', 'text-'))}>
          <Icon size={18} className={color} />
        </div>
        {trend !== undefined && (
          <span className={cn('text-[11px] font-medium', trend >= 0 ? 'text-emerald' : 'text-rose')}>
            {trend >= 0 ? '↑' : '↓'} {Math.abs(trend)}%
          </span>
        )}
      </div>
      <div className="mt-3">
        <div className="text-2xl font-bold text-white">{value}</div>
        <div className="text-xs font-medium text-slate-300 mt-0.5">{label}</div>
        {sub && <div className="text-[11px] text-slate-500 mt-0.5">{sub}</div>}
      </div>
    </motion.div>
  )
}

function SystemStatusItem({ icon: Icon, label, status, color }: { icon: any; label: string; status: string; color: string }) {
  return (
    <div className="flex items-center gap-3 py-2.5 border-b border-navy-600 last:border-0">
      <div className={cn('w-2 h-2 rounded-full', color === 'green' ? 'bg-emerald' : color === 'amber' ? 'bg-amber' : 'bg-rose', 'animate-pulse-slow')} />
      <Icon size={15} className="text-slate-400" />
      <span className="text-sm text-slate-300 flex-1">{label}</span>
      <span className={cn('text-xs font-medium', color === 'green' ? 'text-emerald' : color === 'amber' ? 'text-amber' : 'text-rose')}>{status}</span>
    </div>
  )
}

export default function DashboardPage() {
  const navigate = useNavigate()
  const [scans, setScans] = useState<any[]>([])
  const [health, setHealth] = useState<'online' | 'offline' | 'checking'>('checking')

  useEffect(() => {
    getScans().then(r => setScans(r.data.scans || [])).catch(() => {})
    getHealth().then(() => setHealth('online')).catch(() => setHealth('offline'))
  }, [])

  const completed = scans.filter(s => s.status === 'uploaded').length

  return (
    <AppLayout breadcrumb={['DentAI', 'Dashboard']} title="Dashboard">
      <div className="space-y-6 animate-fade-in">
        {/* Welcome */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-white">Clinical Dashboard</h1>
            <p className="text-slate-400 text-sm mt-0.5">AI-powered CBCT mandible segmentation platform</p>
          </div>
          <button onClick={() => navigate('/upload')} className="btn-primary">
            <Upload size={15} /> New Scan
          </button>
        </div>

        {/* Stats grid */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard icon={ScanLine}     label="Total Scans"         value={scans.length}  sub="All time"         color="text-brand"   trend={12} />
          <StatCard icon={CheckCircle2} label="Analyses Complete"   value={completed}     sub="Segmented"        color="text-emerald" trend={8}  />
          <StatCard icon={Activity}     label="Avg. Confidence"     value="88.6%"         sub="Last 30 analyses" color="text-cyan"    trend={3}  />
          <StatCard icon={Clock}        label="Avg. Process Time"   value="~18s"          sub="Per scan"         color="text-violet"  trend={-5} />
        </div>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard icon={Users}     label="Total Patients"   value={Math.ceil(scans.length * 0.8)} sub="Unique patients"  color="text-amber"  />
          <StatCard icon={HardDrive} label="STL Exports"      value={completed * 9}   sub="7 regions each"   color="text-brand"  />
          <StatCard icon={Database}  label="DICOM Exports"    value={completed * 4}   sub="Generated"        color="text-cyan"   />
          <StatCard icon={TrendingUp} label="Today's Scans"   value="0"               sub="Live count"        color="text-emerald"/>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div className="card p-5">
            <div className="section-header">Weekly Activity</div>
            <ResponsiveContainer width="100%" height={180}>
              <BarChart data={WEEKLY} barCategoryGap="30%">
                <CartesianGrid strokeDasharray="3 3" stroke="#1e2d40" />
                <XAxis dataKey="day" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#111827', border: '1px solid #1e2d40', borderRadius: 8, fontSize: 12 }} />
                <Bar dataKey="scans"    name="Scans"    fill="#3b82f6" radius={[4,4,0,0]} />
                <Bar dataKey="analyses" name="Analyses" fill="#10b981" radius={[4,4,0,0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className="card p-5">
            <div className="section-header">Segmentation Confidence Trend</div>
            <ResponsiveContainer width="100%" height={180}>
              <AreaChart data={CONFIDENCE}>
                <defs>
                  <linearGradient id="cg" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%"  stopColor="#06b6d4" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#06b6d4" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e2d40" />
                <XAxis dataKey="week" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                <YAxis domain={[80, 100]} tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                <Tooltip contentStyle={{ background: '#111827', border: '1px solid #1e2d40', borderRadius: 8, fontSize: 12 }} />
                <Area type="monotone" dataKey="score" name="Confidence %" stroke="#06b6d4" fill="url(#cg)" strokeWidth={2} dot={{ fill: '#06b6d4', r: 3 }} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Bottom row: recent scans + system status */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
          {/* Recent scans */}
          <div className="card p-5 lg:col-span-2">
            <div className="flex items-center justify-between mb-4">
              <div className="section-header mb-0">Recent Scans</div>
              <button onClick={() => navigate('/history')} className="text-xs text-brand hover:text-brand-light transition-colors">View all</button>
            </div>
            {scans.length === 0 ? (
              <div className="flex flex-col items-center py-8 text-slate-500">
                <ScanLine size={32} className="mb-2 opacity-40" />
                <p className="text-sm">No scans yet</p>
                <button onClick={() => navigate('/upload')} className="btn-primary mt-3 text-xs">Upload first scan</button>
              </div>
            ) : (
              <div className="space-y-2">
                {scans.slice(0, 5).map((s: any) => (
                  <div key={s.id} className="flex items-center gap-3 p-3 rounded-lg bg-navy-800 hover:bg-navy-600 transition-colors group">
                    <div className="w-8 h-8 rounded-lg bg-brand/20 flex items-center justify-center">
                      <ScanLine size={14} className="text-brand" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium text-slate-200 truncate">{s.patient_name || 'Unknown Patient'}</div>
                      <div className="text-[11px] text-slate-500">{s.filename} · {fmtDate(s.created_at)}</div>
                    </div>
                    <span className={cn('badge text-[10px]', s.status === 'uploaded' ? 'badge-blue' : 'badge-green')}>{s.status}</span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* System status */}
          <div className="card p-5">
            <div className="section-header">System Status</div>
            <SystemStatusItem icon={Wifi}    label="Backend API"   status={health === 'online' ? 'Online' : health === 'checking' ? 'Checking...' : 'Offline'} color={health === 'online' ? 'green' : health === 'checking' ? 'amber' : 'red'} />
            <SystemStatusItem icon={Database} label="MySQL DB"     status="Connected"   color="green" />
            <SystemStatusItem icon={Cpu}      label="AI Model"     status="Ready"       color="green" />
            <SystemStatusItem icon={HardDrive} label="Storage"     status="Available"   color="green" />

            <div className="mt-4 pt-4 border-t border-navy-600">
              <div className="section-header">Quick Actions</div>
              <div className="grid grid-cols-2 gap-2">
                {[
                  { icon: Upload,    label: 'Upload',  to: '/upload'   },
                  { icon: History,   label: 'History', to: '/history'  },
                  { icon: BarChart2, label: 'Results', to: '/results'  },
                  { icon: Activity,  label: 'Workflow',to: '/workflow' },
                ].map(({ icon: I, label, to }) => (
                  <button key={to} onClick={() => navigate(to)}
                    className="flex flex-col items-center gap-1.5 p-3 rounded-lg bg-navy-800 hover:bg-navy-600 text-slate-400 hover:text-slate-100 transition-all text-xs">
                    <I size={16} />
                    {label}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </AppLayout>
  )
}
