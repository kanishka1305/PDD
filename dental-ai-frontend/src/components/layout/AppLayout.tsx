import { ReactNode } from 'react'
import { Navigate } from 'react-router-dom'
import Sidebar from './Sidebar'
import Header from './Header'
import { store } from '@/lib/store'

interface Props {
  children: ReactNode
  breadcrumb?: string[]
  title?: string
  scanId?: number | null
}

export default function AppLayout({ children, breadcrumb = ['DentAI'], title = '', scanId }: Props) {
  const user = store.getUser()
  if (!user) return <Navigate to="/login" replace />

  return (
    <div className="flex h-screen bg-navy-900 overflow-hidden">
      <Sidebar user={user} />
      <div className="flex flex-col flex-1 min-w-0 overflow-hidden">
        <Header breadcrumb={breadcrumb} title={title} scanId={scanId} />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  )
}
