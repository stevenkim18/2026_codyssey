import { Navigate, Outlet, useLocation } from "react-router"
import LoadingState from "./LoadingState"
import { useAuth } from "../contexts/useAuth"

function ProtectedRoute() {
  const { user, isLoading } = useAuth()
  const location = useLocation()

  if (isLoading) {
    return <LoadingState message="인증 상태를 확인하고 있습니다..." fullPage />
  }

  if (!user) {
    return <Navigate to="/login" replace state={{ from: `${location.pathname}${location.search}` }} />
  }

  return <Outlet />
}

export default ProtectedRoute
