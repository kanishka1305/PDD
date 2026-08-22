import { NavLink, useNavigate } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import {
  LayoutDashboard, Upload, BarChart2, GitBranch, Clock,
  LogOut, ChevronLeft, ChevronRight, Cpu, Settings, Activity
} from 'lucide-react'
import { store, User } from '@/lib/store'
import { cn, getInitials } from '@/lib/utils'
import { useState } from 'react'

const NAV = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/upload',    icon: Upload,          label: 'Upload Scan' },
  { to: '/results',   icon: BarChart2,       label: 'Results' },
  { to: '/workflow',  icon: Activity,        label: 'Workflow' },
  { to: '/history',   icon: Clock,           label: 'History' },
]

export default function Sidebar({ user }: { user: User }) {
  const navigate = useNavigate()
  const [collapsed, setCollapsed] = useState(false)

  const logout = () => { store.clear(); navigate('/login') }

  return (
    <motion.aside
      initial={false}
      animate={{ width: collapsed ? 68 : 240 }}
      transition={{ type: 'spring', stiffness: 300, damping: 30 }}
      className="relative flex flex-col h-screen bg-navy-800 border-r border-navy-500 z-20 overflow-hidden shrink-0"
    >
      {/* Logo */}
      <div className={cn('flex items-center h-16 px-4 border-b border-navy-500 gap-3', collapsed && 'justify-center px-0')}>
        <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-brand to-cyan flex items-center justify-center shrink-0">
          <Cpu size={16} className="text-white" />
        </div>
        <AnimatePresence>
          {!collapsed && (
            <motion.div initial={{ opacity: 0, x: -10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -10 }}>
              <div className="font-bold text-white text-sm leading-none">DentAI</div>
              <div className="text-[10px] text-slate-400 mt-0.5">CBCT Platform</div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Nav */}
      <nav className="flex-1 py-4 px-2 space-y-1 overflow-y-auto">
        {NAV.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            title={collapsed ? label : undefined}
            className={({ isActive }) => cn(
              'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-150 group',
              isActive
                ? 'bg-brand/20 text-brand border border-brand/30'
                : 'text-slate-400 hover:text-slate-100 hover:bg-navy-600',
              collapsed && 'justify-center px-0'
            )}
          >
            {({ isActive }) => (
              <>
                <Icon size={18} className={cn('shrink-0', isActive ? 'text-brand' : 'text-slate-400 group-hover:text-slate-200')} />
                <AnimatePresence>
                  {!collapsed && (
                    <motion.span initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="truncate">
                      {label}
                    </motion.span>
                  )}
                </AnimatePresence>
                {isActive && !collapsed && (
                  <motion.div layoutId="activeIndicator" className="ml-auto w-1.5 h-1.5 rounded-full bg-brand" />
                )}
              </>
            )}
          </NavLink>
        ))}
      </nav>

      {/* Bottom: user + settings + logout */}
      <div className="border-t border-navy-500 p-3 space-y-2">
        <button
          title={collapsed ? 'Settings' : undefined}
          className={cn('flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-400 hover:text-slate-100 hover:bg-navy-600 w-full transition-all', collapsed && 'justify-center px-0')}
        >
          <Settings size={16} className="shrink-0" />
          {!collapsed && <span>Settings</span>}
        </button>

        <div className={cn('flex items-center gap-3 px-3 py-2 rounded-lg bg-navy-700', collapsed && 'justify-center px-0')}>
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-brand to-violet flex items-center justify-center text-white text-xs font-bold shrink-0">
            {getInitials(user.name)}
          </div>
          <AnimatePresence>
            {!collapsed && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} className="flex-1 min-w-0">
                <div className="text-xs font-semibold text-slate-100 truncate">Dr. {user.name}</div>
                <div className="text-[10px] text-slate-400 truncate">{user.email}</div>
              </motion.div>
            )}
          </AnimatePresence>
          {!collapsed && (
            <button onClick={logout} title="Sign out" className="text-slate-500 hover:text-rose transition-colors">
              <LogOut size={14} />
            </button>
          )}
        </div>
      </div>

      {/* Collapse toggle */}
      <button
        onClick={() => setCollapsed(c => !c)}
        className="absolute -right-3 top-20 w-6 h-6 rounded-full bg-navy-600 border border-navy-400 flex items-center justify-center text-slate-400 hover:text-slate-100 hover:bg-navy-500 transition-all z-30 shadow-card"
      >
        {collapsed ? <ChevronRight size={12} /> : <ChevronLeft size={12} />}
      </button>
    </motion.aside>
  )
}
