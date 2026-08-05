import type { TaskPriority, TaskStatus } from "../types/database"

type StatusBadgeProps =
  | { type: "status"; value: TaskStatus }
  | { type: "priority"; value: TaskPriority }

const statusLabels: Record<TaskStatus, string> = {
  todo: "할 일",
  in_progress: "진행 중",
  done: "완료",
}

const priorityLabels: Record<TaskPriority, string> = {
  low: "낮음",
  medium: "보통",
  high: "높음",
}

function StatusBadge(props: StatusBadgeProps) {
  const isStatus = props.type === "status"
  const label = isStatus ? statusLabels[props.value] : priorityLabels[props.value]
  const color = isStatus
    ? props.value === "done"
      ? "bg-emerald-50 text-emerald-700"
      : props.value === "in_progress"
        ? "bg-blue-50 text-blue-700"
        : "bg-slate-100 text-slate-600"
    : props.value === "high"
      ? "bg-red-50 text-red-700"
      : props.value === "medium"
        ? "bg-amber-50 text-amber-700"
        : "bg-slate-100 text-slate-600"

  return <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${color}`}>{label}</span>
}

export default StatusBadge
