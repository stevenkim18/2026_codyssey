import { Route, Routes } from "react-router"
import AppLayout from "./layouts/AppLayout"
import DashboardPage from "./pages/DashboardPage"
import LandingPage from "./pages/LandingPage"
import LoginPage from "./pages/LoginPage"
import NotFoundPage from "./pages/NotFoundPage"
import ProjectDetailPage from "./pages/ProjectDetailPage"
import ProjectEditPage from "./pages/ProjectEditPage"
import ProjectListPage from "./pages/ProjectListPage"
import ProjectNewPage from "./pages/ProjectNewPage"
import SignupPage from "./pages/SignupPage"
import TaskDetailPage from "./pages/TaskDetailPage"
import TaskEditPage from "./pages/TaskEditPage"
import TaskNewPage from "./pages/TaskNewPage"
import ProtectedRoute from "./components/ProtectedRoute"

function App() {
  return (
    <Routes>
      <Route element={<AppLayout />}>
        <Route path="/" element={<LandingPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />
        <Route element={<ProtectedRoute />}>
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/projects" element={<ProjectListPage />} />
          <Route path="/projects/new" element={<ProjectNewPage />} />
          <Route path="/projects/:id" element={<ProjectDetailPage />} />
          <Route path="/projects/:id/edit" element={<ProjectEditPage />} />
          <Route path="/projects/:id/tasks/new" element={<TaskNewPage />} />
          <Route path="/tasks/:id" element={<TaskDetailPage />} />
          <Route path="/tasks/:id/edit" element={<TaskEditPage />} />
        </Route>
        <Route path="*" element={<NotFoundPage />} />
      </Route>
    </Routes>
  )
}

export default App
