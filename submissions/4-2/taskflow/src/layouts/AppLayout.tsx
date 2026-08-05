import { Link, NavLink, Outlet } from "react-router"

function AppLayout() {
  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <Link to="/" className="text-xl font-bold tracking-tight text-slate-950">
            TaskFlow
          </Link>

          <nav className="flex items-center gap-5 text-sm font-medium">
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
            <Link
              to="/login"
              className="rounded-lg bg-slate-900 px-4 py-2 text-white transition hover:bg-slate-700"
            >
              로그인
            </Link>
          </nav>
        </div>
      </header>

      <Outlet />
    </div>
  )
}

export default AppLayout
