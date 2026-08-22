import { Bell, ChevronRight, Search, Settings, User } from 'lucide-react'
import { format } from 'date-fns'
import { store } from '@/lib/store'

interface Props {
  breadcrumb: string[]
  title: string
  scanId?: number | null
}

export default function Header({ breadcrumb, title, scanId }: Props) {
  const user = store.getUser()
  const today = format(new Date(), 'EEE, dd MMM yyyy')

  return (
    <header className="h-14 bg-navy-800/80 backdrop-blur-sm border-b border-navy-500 flex items-center px-6 gap-4 sticky top-0 z-10">
      {/* Breadcrumb */}
      <div className="flex items-center gap-1.5 text-xs text-slate-500 flex-1">
        {breadcrumb.map((b, i) => (
          <span key={i} className="flex items-center gap-1.5">
            {i > 0 && <ChevronRight size={12} className="text-slate-600" />}
            <span className={i === breadcrumb.length - 1 ? 'text-slate-300 font-medium' : ''}>{b}</span>
          </span>
        ))}
      </div>

      {/* Scan badge */}
      {scanId && (
        <div className="badge-blue text-[10px]">
          Scan #{scanId}
        </div>
      )}

      {/* Date */}
      <div className="text-xs text-slate-500 hidden sm:block">{today}</div>

      {/* Actions */}
      <div className="flex items-center gap-1">
        <button className="btn-ghost p-2 relative">
          <Bell size={16} />
          <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 rounded-full bg-brand" />
        </button>
        <button className="btn-ghost p-2">
          <Settings size={16} />
        </button>
        <div className="w-7 h-7 rounded-full bg-gradient-to-br from-brand to-violet flex items-center justify-center text-white text-xs font-bold ml-1 cursor-pointer">
          {user?.name?.charAt(0).toUpperCase() ?? 'D'}
        </div>
      </div>
    </header>
  )
}
