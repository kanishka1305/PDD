import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import './index.css'

import LoginPage from './pages/LoginPage'
import SignupPage from './pages/SignupPage'
import ForgotPasswordPage from './pages/ForgotPasswordPage'
import DashboardPage from './pages/DashboardPage'
import UploadPage from './pages/UploadPage'
import ResultsPage from './pages/ResultsPage'
import WorkflowPage from './pages/WorkflowPage'
import HistoryPage from './pages/HistoryPage'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/"                element={<Navigate to="/login" replace />} />
        <Route path="/login"           element={<LoginPage />} />
        <Route path="/signup"          element={<SignupPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/dashboard"       element={<DashboardPage />} />
        <Route path="/upload"          element={<UploadPage />} />
        <Route path="/results"         element={<ResultsPage />} />
        <Route path="/workflow"        element={<WorkflowPage />} />
        <Route path="/history"         element={<HistoryPage />} />
        <Route path="*"                element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)
