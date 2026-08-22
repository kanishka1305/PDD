import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Eye, EyeOff, Cpu, Lock, Mail, User, Hash, AlertCircle, CheckCircle2 } from 'lucide-react'
import { signup } from '@/lib/api'
import { cn } from '@/lib/utils'

function pwStrength(pw: string) {
  const checks = [pw.length >= 8, /[A-Z]/.test(pw), /[a-z]/.test(pw), /\d/.test(pw), /[@#$%^&+=!]/.test(pw)]
  const score = checks.filter(Boolean).length
  const labels = ['', 'Very Weak', 'Weak', 'Fair', 'Strong', 'Very Strong']
  const colors = ['', 'bg-rose', 'bg-orange-500', 'bg-amber', 'bg-emerald', 'bg-brand']
  return { score, label: labels[score], color: colors[score] }
}

export default function SignupPage() {
  const navigate = useNavigate()
  const [form, setForm] = useState({ name: '', license: '', email: '', password: '' })
  const [showPw, setShowPw] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const strength = pwStrength(form.password)

  const set = (k: keyof typeof form) => (e: React.ChangeEvent<HTMLInputElement>) => setForm(f => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('')
    try {
      const { data } = await signup(form.name, form.license, form.email, form.password)
      if (data.success) { setSuccess(true); setTimeout(() => navigate('/login'), 1500) }
      else setError(data.message || 'Signup failed')
    } catch { setError('Cannot connect to server') }
    finally { setLoading(false) }
  }

  return (
    <div className="min-h-screen bg-navy-900 flex items-center justify-center p-4">
      <div className="absolute inset-0 bg-[linear-gradient(rgba(59,130,246,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(59,130,246,0.03)_1px,transparent_1px)] bg-[size:48px_48px] pointer-events-none" />
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-to-br from-brand to-cyan shadow-glow mb-4">
            <Cpu size={28} className="text-white" />
          </div>
          <h1 className="text-2xl font-bold text-white">DentAI</h1>
          <p className="text-slate-400 text-sm mt-1">Create your clinical account</p>
        </div>

        <div className="card p-8">
          <h2 className="text-lg font-semibold text-white mb-1">Create Account</h2>
          <p className="text-slate-400 text-sm mb-6">Register as a dental professional</p>

          {error && (
            <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }}
              className="flex items-center gap-2 p-3 rounded-lg bg-rose/10 border border-rose/30 text-rose text-sm mb-4">
              <AlertCircle size={15} className="shrink-0" /> {error}
            </motion.div>
          )}
          {success && (
            <motion.div initial={{ opacity: 0, y: -8 }} animate={{ opacity: 1, y: 0 }}
              className="flex items-center gap-2 p-3 rounded-lg bg-emerald/10 border border-emerald/30 text-emerald text-sm mb-4">
              <CheckCircle2 size={15} className="shrink-0" /> Account created! Redirecting to login...
            </motion.div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="label">Full Name</label>
              <div className="relative">
                <User size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <input className="input pl-9" type="text" placeholder="Dr. Jane Smith" value={form.name} onChange={set('name')} required />
              </div>
            </div>
            <div>
              <label className="label">Medical License Number</label>
              <div className="relative">
                <Hash size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <input className="input pl-9" type="text" placeholder="MED-123456" value={form.license} onChange={set('license')} required />
              </div>
            </div>
            <div>
              <label className="label">Email Address</label>
              <div className="relative">
                <Mail size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <input className="input pl-9" type="email" placeholder="doctor@hospital.com" value={form.email} onChange={set('email')} required />
              </div>
            </div>
            <div>
              <label className="label">Password</label>
              <div className="relative">
                <Lock size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                <input className="input pl-9 pr-10" type={showPw ? 'text' : 'password'} placeholder="Min 8 chars, 1 upper, 1 number, 1 special" value={form.password} onChange={set('password')} required />
                <button type="button" onClick={() => setShowPw(p => !p)} className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-500 hover:text-slate-300 transition-colors">
                  {showPw ? <EyeOff size={16} /> : <Eye size={16} />}
                </button>
              </div>
              {form.password && (
                <div className="mt-2">
                  <div className="flex gap-1 mb-1">
                    {[1,2,3,4,5].map(i => (
                      <div key={i} className={cn('h-1 flex-1 rounded-full transition-all duration-300', i <= strength.score ? strength.color : 'bg-navy-500')} />
                    ))}
                  </div>
                  <p className="text-[11px] text-slate-400">{strength.label}</p>
                </div>
              )}
            </div>
            <button type="submit" disabled={loading || success} className={cn('btn-primary w-full justify-center py-2.5 mt-2', (loading || success) && 'opacity-70 cursor-not-allowed')}>
              {loading ? <><span className="w-4 h-4 rounded-full border-2 border-white/30 border-t-white animate-spin" /> Creating...</> : 'Create Account'}
            </button>
          </form>

          <div className="mt-6 pt-5 border-t border-navy-500 text-center text-sm text-slate-500">
            Already have an account?{' '}
            <Link to="/login" className="text-brand hover:text-brand-light font-medium transition-colors">Sign in</Link>
          </div>
        </div>
      </motion.div>
    </div>
  )
}
