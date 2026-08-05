import { Link } from "react-router"
import type { Project } from "../types/database"

type ProjectCardProps = {
  project: Project
  taskCount?: number
}

function ProjectCard({ project, taskCount = 0 }: ProjectCardProps) {
  return (
    <Link
      to={`/projects/${project.id}`}
      className="group rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:-translate-y-0.5 hover:border-blue-300 hover:shadow-md"
    >
      <div className="mb-5 flex items-start justify-between gap-4">
        <span className={`h-3 w-3 rounded-full ${projectColorClass[project.color ?? "blue"]}`} aria-hidden="true" />
        <span className="text-xs text-slate-400">{taskCount}개 할 일</span>
      </div>
      <h2 className="text-lg font-semibold text-slate-950 group-hover:text-blue-600">
        {project.name}
      </h2>
      <p className="mt-2 line-clamp-2 text-sm text-slate-500">
        {project.description || "프로젝트 설명이 없습니다."}
      </p>
    </Link>
  )
}

const projectColorClass: Record<string, string> = {
  blue: "bg-blue-500",
  green: "bg-emerald-500",
  yellow: "bg-amber-400",
  red: "bg-red-500",
  purple: "bg-purple-500",
  gray: "bg-slate-400",
}

export default ProjectCard
