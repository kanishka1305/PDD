import { useCallback, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Upload, File, X, CheckCircle2, Loader2, AlertCircle, CloudUpload, Cpu, Layers, FileText, Zap } from 'lucide-react'
import AppLayout from '@/components/layout/AppLayout'
import { uploadScan, analyzeScan } from '@/lib/api'
import { store } from '@/lib/store'
import { cn, fmtNumber } from '@/lib/utils'

const PIPELINE = [
  { id: 'upload',    label: 'Upload & Validation',    icon: CloudUpload  },
  { id: 'preproc',   label: 'Preprocessing',           icon: Layers       },
  { id: 'norm',      label: 'Normalization',            icon: Zap          },
  { id: 'segment',   label: 'AI Segmentation',         icon: Cpu          },
  { id: 'volume',    label: 'Volume Calculation',       icon: FileText     },
  { id: 'stl',       label: 'STL Generation (7 regions)', icon: Layers    },
  { id: 'report',    label: 'Report Generation',        icon: FileText     },
  { id: 'done',      label: 'Completed',                icon: CheckCircle2 },
]

type Phase = 'idle' | 'uploading' | 'analysing' | 'done' | 'error'

export default function UploadPage() {
  const navigate = useNavigate()
  const [file, setFile] = useState<File | null>(null)
  const [dragging, setDragging] = useState(false)
  const [phase, setPhase] = useState<Phase>('idle')
  const [progress, setProgress] = useState(0)
  const [pipelineStep, setPipelineStep] = useState(-1)
  const [scanId, setScanId] = useState<number | null>(null)
  const [meta, setMeta] = useState<any>(null)
  const [error, setError] = useState('')
  const [elapsedMs, setElapsedMs] = useState(0)

  const onDrop = useCallback((f: File) => {
    if (!f.name.match(/\.(dcm|nii|nii\.gz|zip)$/i)) {
      setError('Unsupported format. Please upload .dcm, .nii, .nii.gz or .zip files.')
      return
    }
    setFile(f); setError(''); setPhase('idle')
  }, [])

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault(); setDragging(false)
    if (e.dataTransfer.files[0]) onDrop(e.dataTransfer.files[0])
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) onDrop(e.target.files[0])
  }

  const runUpload = async () => {
    if (!file) return
    setPhase('uploading'); setProgress(0); setError('')
    const start = Date.now()
    const timer = setInterval(() => setElapsedMs(Date.now() - start), 500)
    try {
      // Animate progress bar
      let p = 0
      const tick = setInterval(() => { p = Math.min(p + 6, 85); setProgress(p) }, 200)
      const { data } = await uploadScan(file)
      clearInterval(tick); setProgress(100)

      if (data.error) { setError(data.error); setPhase('error'); clearInterval(timer); return }
      setScanId(data.scan_id); setMeta(data.metadata)
      setPhase('analysing')

      // Animate pipeline steps
      for (let i = 0; i < PIPELINE.length - 1; i++) {
        setPipelineStep(i)
        await new Promise(r => setTimeout(r, 900 + Math.random() * 600))
      }

      const { data: result } = await analyzeScan(data.scan_id)
      if (result.error) { setError(result.error); setPhase('error'); clearInterval(timer); return }

      store.setResult(result)
      setPipelineStep(PIPELINE.length - 1)
      setPhase('done')
      clearInterval(timer)
    } catch (e: any) {
      setError(e?.response?.data?.detail || e?.message || 'Processing failed')
      setPhase('error')
      clearInterval(timer)
    }
  }

  return (
    <AppLayout breadcrumb={['DentAI', 'Upload Scan']} title="Upload Scan">
      <div className="max-w-3xl mx-auto space-y-6 animate-fade-in">
        <div>
          <h1 className="text-xl font-bold text-white">Upload CBCT Scan</h1>
          <p className="text-slate-400 text-sm mt-1">Supported formats: DICOM (.dcm), NIfTI (.nii, .nii.gz), ZIP archive</p>
        </div>

        {/* Upload zone */}
        {phase === 'idle' && (
          <div
            onDragOver={e => { e.preventDefault(); setDragging(true) }}
            onDragLeave={() => setDragging(false)}
            onDrop={handleDrop}
            onClick={() => !file && document.getElementById('file-input')?.click()}
            className={cn(
              'relative border-2 border-dashed rounded-xl p-12 text-center transition-all duration-200 cursor-pointer',
              dragging ? 'border-brand bg-brand/10 scale-[1.01]' : 'border-navy-400 bg-navy-800/50 hover:border-brand/50 hover:bg-navy-700/50',
              file && 'cursor-default'
            )}
          >
            <input id="file-input" type="file" accept=".dcm,.nii,.nii.gz,.zip" className="hidden" onChange={handleFileChange} />
            {!file ? (
              <>
                <motion.div animate={{ y: dragging ? -8 : 0 }} className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-brand/20 mb-4">
                  <Upload size={32} className="text-brand" />
                </motion.div>
                <h3 className="text-base font-semibold text-white mb-2">Drop your scan file here</h3>
                <p className="text-slate-400 text-sm mb-4">or click to browse from your computer</p>
                <div className="flex items-center justify-center gap-2 flex-wrap">
                  {['.dcm', '.nii', '.nii.gz', '.zip'].map(f => (
                    <span key={f} className="badge-blue text-[11px]">{f}</span>
                  ))}
                </div>
              </>
            ) : (
              <div className="flex items-center gap-4">
                <div className="w-12 h-12 rounded-xl bg-brand/20 flex items-center justify-center shrink-0">
                  <File size={24} className="text-brand" />
                </div>
                <div className="flex-1 text-left">
                  <div className="font-semibold text-white">{file.name}</div>
                  <div className="text-sm text-slate-400 mt-0.5">{(file.size / 1024).toFixed(1)} KB · Ready to process</div>
                </div>
                <button onClick={e => { e.stopPropagation(); setFile(null) }} className="text-slate-500 hover:text-rose transition-colors">
                  <X size={18} />
                </button>
              </div>
            )}
          </div>
        )}

        {error && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
            className="flex items-start gap-2 p-4 rounded-xl bg-rose/10 border border-rose/30 text-rose text-sm">
            <AlertCircle size={16} className="shrink-0 mt-0.5" />
            <div><p className="font-medium">Error</p><p className="text-rose/80 mt-0.5">{error}</p></div>
          </motion.div>
        )}

        {/* Action button */}
        {phase === 'idle' && file && (
          <motion.div initial={{ opacity: 0, y: 8 }} animate={{ opacity: 1, y: 0 }}>
            <div className="card p-5 mb-4">
              <h3 className="text-sm font-semibold text-white mb-3">Processing Pipeline</h3>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
                {PIPELINE.slice(0, 4).map(({ label, icon: Icon }) => (
                  <div key={label} className="flex items-center gap-2 text-xs text-slate-400 p-2 bg-navy-800 rounded-lg">
                    <Icon size={13} className="text-brand shrink-0" /> <span className="truncate">{label}</span>
                  </div>
                ))}
              </div>
              <p className="text-xs text-slate-500 mt-3">Estimated time: 15–30 seconds depending on scan size</p>
            </div>
            <button onClick={runUpload} className="btn-primary w-full justify-center py-3 text-base">
              <Cpu size={18} /> Run AI Segmentation
            </button>
          </motion.div>
        )}

        {/* Upload progress */}
        {phase === 'uploading' && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="card p-6 space-y-4">
            <div className="flex items-center gap-3">
              <Loader2 size={20} className="text-brand animate-spin" />
              <span className="font-semibold text-white">Uploading scan...</span>
              <span className="ml-auto text-sm text-brand font-mono">{progress}%</span>
            </div>
            <div className="h-2 bg-navy-800 rounded-full overflow-hidden">
              <motion.div className="h-full bg-gradient-to-r from-brand to-cyan rounded-full" style={{ width: `${progress}%` }} transition={{ duration: 0.3 }} />
            </div>
          </motion.div>
        )}

        {/* Analysis pipeline */}
        {phase === 'analysing' && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="card p-6">
            <div className="flex items-center justify-between mb-5">
              <div>
                <h3 className="font-semibold text-white">AI Processing Pipeline</h3>
                <p className="text-xs text-slate-400 mt-0.5">Scan ID #{scanId} · {(elapsedMs / 1000).toFixed(1)}s elapsed</p>
              </div>
              <Loader2 size={20} className="text-brand animate-spin" />
            </div>
            <div className="space-y-2">
              {PIPELINE.map(({ id, label, icon: Icon }, i) => {
                const done = i < pipelineStep
                const active = i === pipelineStep
                return (
                  <motion.div key={id}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: i <= pipelineStep + 1 ? 1 : 0.3, x: 0 }}
                    className={cn('flex items-center gap-3 p-3 rounded-lg transition-all', active ? 'bg-brand/15 border border-brand/30' : done ? 'bg-navy-800' : 'bg-navy-800/40')}
                  >
                    <div className={cn('w-7 h-7 rounded-lg flex items-center justify-center shrink-0', done ? 'bg-emerald/20' : active ? 'bg-brand/20' : 'bg-navy-600')}>
                      {done ? <CheckCircle2 size={14} className="text-emerald" />
                             : active ? <Loader2 size={14} className="text-brand animate-spin" />
                             : <Icon size={14} className="text-slate-500" />}
                    </div>
                    <span className={cn('text-sm', done ? 'text-emerald' : active ? 'text-white font-medium' : 'text-slate-500')}>
                      {label}
                    </span>
                    {done && <span className="ml-auto text-[10px] text-emerald">✓</span>}
                    {active && <span className="ml-auto text-[10px] text-brand animate-pulse">Running...</span>}
                  </motion.div>
                )
              })}
            </div>
          </motion.div>
        )}

        {/* Done */}
        {phase === 'done' && (
          <motion.div initial={{ opacity: 0, scale: 0.95 }} animate={{ opacity: 1, scale: 1 }} className="card p-8 text-center">
            <motion.div initial={{ scale: 0 }} animate={{ scale: 1 }} transition={{ delay: 0.2, type: 'spring' }}
              className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-emerald/20 mb-4">
              <CheckCircle2 size={32} className="text-emerald" />
            </motion.div>
            <h3 className="text-xl font-bold text-white mb-1">Analysis Complete!</h3>
            <p className="text-slate-400 text-sm mb-2">Scan #{scanId} has been segmented into 7 anatomical mandible regions.</p>
            {meta && <p className="text-xs text-slate-500 mb-6">{meta.modality || 'CT'} · {meta.patient_name || 'Patient'} · {(elapsedMs/1000).toFixed(1)}s</p>}
            <div className="flex items-center justify-center gap-3">
              <button onClick={() => navigate('/results')} className="btn-primary px-8">View Results & Export</button>
              <button onClick={() => { setFile(null); setPhase('idle'); setError('') }} className="btn-secondary">Upload Another</button>
            </div>
          </motion.div>
        )}

        {/* Error retry */}
        {phase === 'error' && (
          <div className="flex items-center justify-center gap-3">
            <button onClick={() => { setPhase('idle'); setError('') }} className="btn-secondary">← Try Again</button>
            <button onClick={runUpload} className="btn-primary">Retry Analysis</button>
          </div>
        )}
      </div>
    </AppLayout>
  )
}
