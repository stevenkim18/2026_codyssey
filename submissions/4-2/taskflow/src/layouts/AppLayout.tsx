import { Link, NavLink, Outlet, useNavigate } from "react-router"
import { useAuth } from "../contexts/useAuth"

function AppLayout() {
  const { user, isLoading, signOut } = useAuth()
  const navigate = useNavigate()

  async function handleSignOut() {
    await signOut()
    navigate("/login")
  }

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link to="/" className="text-xl font-bold tracking-tight text-slate-950">
            TaskFlow
          </Link>

          <nav className="flex items-center gap-5 text-sm font-medium">
            {user && (
              <>
                <NavLink
                  to="/dashboard"
                  className={({ isActive }) =>
                    isActive ? "text-blue-600" : "text-slate-500 hover:text-slate-900"
                  }
                >
                  대시보드
                </NavLink>
                <NavLink
                  to="/projects"
                  className={({ isActive }) =>
                    isActive ? "text-blue-600" : "text-slate-500 hover:text-slate-900"
                  }
                >
                  프로젝트
                </NavLink>
                <span className="hidden max-w-40 truncate text-slate-400 sm:inline">{user.email}</span>
                <button
                  className="rounded-lg border border-slate-300 px-3 py-2 text-slate-700 transition hover:border-slate-400"
                  type="button"
                  onClick={() => void handleSignOut()}
                >
                  로그아웃
                </button>
              </>
            )}
            {!isLoading && !user && (
              <Link
                to="/login"
                className="rounded-lg bg-slate-900 px-4 py-2 text-white transition hover:bg-slate-700"
              >
                로그인
              </Link>
            )}
          </nav>
        </div>
      </header>

      <Outlet />
    </div>
  )
}

export default AppLayout
