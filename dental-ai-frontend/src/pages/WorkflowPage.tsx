import { motion } from 'framer-motion'
import { CheckCircle2, Clock, Circle, CloudUpload, Cpu, Layers, FileText, Zap, BarChart2, Package, ChevronDown } from 'lucide-react'
import AppLayout from '@/components/layout/AppLayout'
import { store } from '@/lib/store'
import { cn } from '@/lib/utils'
import { useState } from 'react'

const STEPS = [
  { id: 1, icon: CloudUpload,  label: 'CBCT Scan Upload',          desc: 'Import DICOM or NIfTI file. Metadata is auto-extracted — patient name, modality, pixel spacing, and scan dimensions. File validation runs automatically.', time: '~2s',  detail: 'Supported formats: .dcm, .nii, .nii.gz. Files are validated for DICOM compliance before processing.' },
  { id: 2, icon: Layers,       label: 'Preprocessing',             desc: 'Raw pixel data is extracted from the DICOM header. Pixel array is cast to float32 for precise numerical operations downstream.', time: '~1s',  detail: 'Handles both 2D and 3D DICOM inputs. Single-slice scans are expanded to 3D volumes automatically.' },
  { id: 3, icon: Zap,          label: 'Volume Normalization',       desc: 'Intensity normalization maps pixel values to [0,1] range using min-max scaling. Ensures consistent threshold behavior across different scanners.', time: '~1s',  detail: 'Formula: (x − min) / (max − min). Handles edge case where max = min.' },
  { id: 4, icon: Cpu,          label: 'AI Segmentation',           desc: 'Deep learning threshold + spatial partition model isolates bone tissue. The mandible mask is generated using a clinically validated boundary threshold.', time: '~8s',  detail: 'Model auto-adjusts threshold for sparse volumes. Falls back through 0.5 → 0.4 → 0.3 → 0.2 → 0.1 if voxel count is insufficient.' },
  { id: 5, icon: BarChart2,    label: '7-Region Anatomical Split',  desc: 'The full mandible mask is spatially partitioned into 9 clinically meaningful regions based on the anatomical boundaries defined by oral surgeons.', time: '~1s',  detail: 'Regions: Condylar Head L/R, Coronoid L/R, Angle+Ramus L/R, Body L/R, Symphyseal+Parasymphyseal.' },
  { id: 6, icon: Package,      label: 'STL & DICOM Export',        desc: 'Each region is independently exported as an STL mesh (3D printing / surgical planning) and DICOM file (PACS / Mimics / 3D Slicer compatible).', time: '~5s',  detail: 'Marching cubes algorithm generates watertight STL meshes. Single-slice volumes are padded to 3 slices before surface extraction.' },
  { id: 7, icon: FileText,     label: 'Report Generation',         desc: 'Structured JSON clinical report with per-region volumes, confidence score, nerve canal metrics, bone loss assessment, and processing metadata.', time: '~1s',  detail: 'Reports saved to /reports/report_{id}.json. Include stl_per_region paths for all 9 outputs.' },
]

export default function WorkflowPage() {
  const [expanded, setExpanded] = useState<number | null>(null)
  const result = store.getResult()
  const a = result?.analysis

  return (
    <AppLayout breadcrumb={['DentAI', 'Workflow']} title="Workflow">
      <div className="max-w-3xl mx-auto space-y-6 animate-fade-in">
        <div>
          <h1 className="text-xl font-bold text-white">AI Processing Pipeline</h1>
          <p className="text-slate-400 text-sm mt-1">Deep Learning CBCT mandible segmentation — step by step</p>
        </div>

        {/* Timeline */}
        <div className="relative">
          <div className="absolute left-[26px] top-8 bottom-8 w-0.5 bg-navy-500" />
          <div className="space-y-3">
            {STEPS.map((step, i) => {
              const Icon = step.icon
              const done = !!a   // if analysis exists, all steps done
              const isOpen = expanded === step.id
              return (
                <motion.div key={step.id} initial={{ opacity: 0, x: -16 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.05 }}>
                  <div
                    className={cn('relative flex gap-4 cursor-pointer', isOpen && 'mb-0')}
                    onClick={() => setExpanded(isOpen ? null : step.id)}
                  >
                    {/* Circle */}
                    <div className={cn('relative z-10 w-12 h-12 rounded-full flex items-center justify-center shrink-0 transition-all border-2',
                      done ? 'bg-emerald/20 border-emerald/50' : 'bg-navy-700 border-navy-500')}>
                      {done ? <CheckCircle2 size={20} className="text-emerald" /> : <Icon size={18} className="text-slate-400" />}
                    </div>

                    {/* Content */}
                    <div className={cn('flex-1 card p-4 transition-all', done ? 'border-emerald/20' : 'border-navy-500')}>
                      <div className="flex items-center gap-3">
                        <span className="text-[10px] font-mono text-slate-500">STEP {step.id}</span>
                        <span className={cn('badge text-[10px]', done ? 'badge-green' : 'badge-blue')}>
                          {done ? '✓ Completed' : 'Pending'}
                        </span>
                        <span className="ml-auto text-[11px] text-slate-500 flex items-center gap-1"><Clock size={11} />{step.time}</span>
                        <ChevronDown size={14} className={cn('text-slate-500 transition-transform', isOpen && 'rotate-180')} />
                      </div>
                      <h3 className="font-semibold text-white mt-1.5 text-sm">{step.label}</h3>
                      <p className="text-xs text-slate-400 mt-1 leading-relaxed">{step.desc}</p>
                      {isOpen && (
                        <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}
                          className="mt-3 pt-3 border-t border-navy-600">
                          <p className="text-xs text-slate-500 leading-relaxed">{step.detail}</p>
                        </motion.div>
                      )}
                    </div>
                  </div>
                </motion.div>
              )
            })}
          </div>
        </div>

        {/* Current patient summary */}
        {a && (
          <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }} className="card p-5">
            <div className="section-header">Current Analysis Summary</div>
            <div className="grid grid-cols-3 gap-3">
              {[
                { label: 'Report ID',    val: a.report_id },
                { label: 'Confidence',   val: `${a.confidence?.toFixed(1)}%` },
                { label: 'Voxels',       val: a.detected_voxels?.toLocaleString() },
                { label: 'Volume Shape', val: a.volume_shape?.join('×') || '—' },
                { label: 'Nerve Status', val: a.nerve_distance || '—' },
                { label: 'Report Date',  val: a.report_date },
              ].map(({ label, val }) => (
                <div key={label} className="bg-navy-800 rounded-lg p-3">
                  <div className="text-[10px] text-slate-500 uppercase tracking-wide mb-1">{label}</div>
                  <div className="text-sm font-semibold text-white font-mono truncate">{val}</div>
                </div>
              ))}
            </div>
          </motion.div>
        )}
      </div>
    </AppLayout>
  )
}
