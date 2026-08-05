export type TaskStatus = "todo" | "in_progress" | "done"

export type TaskPriority = "low" | "medium" | "high"

export type ProjectColor = "blue" | "green" | "yellow" | "red" | "purple" | "gray"

export type Project = {
  id: string
  user_id: string
  name: string
  description: string | null
  color: string | null
  is_archived: boolean
  created_at: string
  updated_at: string
}

export type Task = {
  id: string
  user_id: string
  project_id: string
  title: string
  description: string | null
  status: TaskStatus
  priority: TaskPriority
  due_date: string | null
  created_at: string
  updated_at: string
}
