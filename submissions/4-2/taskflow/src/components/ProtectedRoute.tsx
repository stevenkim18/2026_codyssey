import { Navigate, Outlet, useLocation } from "react-router"
import { useAuth } from "../contexts/useAuth"

function ProtectedRoute() {
  const { user, isLoading } = useAuth()
  const location = useLocation()

  if (isLoading) {
    return <div className="flex min-h-[calc(100vh-73px)] items-center justify-center text-sm text-slate-500">인증 상태를 확인하고 있습니다...</div>
  }

  if (!user) {
    return <Navigate to="/login" replace state={{ from: `${location.pathname}${location.search}` }} />
  }

  return <Outlet />
}

export default ProtectedRoute
