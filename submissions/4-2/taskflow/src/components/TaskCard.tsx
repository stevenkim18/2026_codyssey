import { Link } from "react-router"
import type { Task } from "../types/database"
import StatusBadge from "./StatusBadge"

type TaskCardProps = {
  task: Task
}

function TaskCard({ task }: TaskCardProps) {
  return (
    <Link
      to={`/tasks/${task.id}`}
      className="block rounded-2xl border border-slate-200 bg-white p-5 shadow-sm transition hover:border-blue-300 hover:shadow-md"
    >
      <div className="flex flex-wrap items-center gap-2">
        <StatusBadge type="status" value={task.status} />
        <StatusBadge type="priority" value={task.priority} />
      </div>
      <h2 className="mt-4 font-semibold text-slate-950">{task.title}</h2>
      <p className="mt-2 line-clamp-2 text-sm text-slate-500">
        {task.description || "상세 설명이 없습니다."}
      </p>
      {task.due_date && <p className="mt-4 text-xs text-slate-400">마감일 {task.due_date}</p>}
    </Link>
  )
}

export default TaskCard
