import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Cpu, Mail, ArrowLeft, AlertCircle, CheckCircle2 } from 'lucide-react'
import { forgotPassword } from '@/lib/api'

export default function ForgotPasswordPage() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [done, setDone] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault(); setLoading(true); setError('')
    try {
      const { data } = await forgotPassword(email)
      if (data.success) {
        if (data.reset_token) {
          navigate(`/reset-password?token=${encodeURIComponent(data.reset_token)}`)
        } else {
          setDone(true)
        }
      } else setError(data.message || 'Error sending reset link')
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
        </div>
        <div className="card p-8">
          <Link to="/login" className="flex items-center gap-1.5 text-slate-400 hover:text-slate-200 text-sm mb-6 transition-colors">
            <ArrowLeft size={15} /> Back to login
          </Link>
          <h2 className="text-lg font-semibold text-white mb-1">Reset Password</h2>
          <p className="text-slate-400 text-sm mb-6">Enter your registered email address and we'll generate a password reset link.</p>

          {error && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              className="flex items-center gap-2 p-3 rounded-lg bg-rose/10 border border-rose/30 text-rose text-sm mb-4">
              <AlertCircle size={15} /> {error}
            </motion.div>
          )}
          {done && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}
              className="flex items-center gap-2 p-3 rounded-lg bg-emerald/10 border border-emerald/30 text-emerald text-sm mb-4">
              <CheckCircle2 size={15} /> Reset link sent. Check your email.
            </motion.div>
          )}

          {!done && (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="label">Email Address</label>
                <div className="relative">
                  <Mail size={15} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                  <input className="input pl-9" type="email" placeholder="doctor@hospital.com" value={email} onChange={e => setEmail(e.target.value)} required />
                </div>
              </div>
              <button type="submit" disabled={loading} className="btn-primary w-full justify-center py-2.5">
                {loading ? <><span className="w-4 h-4 rounded-full border-2 border-white/30 border-t-white animate-spin" /> Sending...</> : 'Send Reset Link'}
              </button>
            </form>
          )}
        </div>
      </motion.div>
    </div>
  )
}
