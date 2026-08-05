import { supabase } from "./supabase"
import type { Task, TaskPriority, TaskStatus } from "../types/database"

const taskFields = "id,user_id,project_id,title,description,status,priority,due_date,created_at,updated_at"

export type TaskInput = {
  project_id: string
  title: string
  description: string | null
  status: TaskStatus
  priority: TaskPriority
  due_date: string | null
}

export async function getTasks() {
  const { data, error } = await supabase
    .from("tasks")
    .select(taskFields)
    .order("created_at", { ascending: false })

  if (error) throw error
  return data as Task[]
}

export async function getTasksByProject(projectId: string) {
  const { data, error } = await supabase
    .from("tasks")
    .select(taskFields)
    .eq("project_id", projectId)
    .order("created_at", { ascending: false })

  if (error) throw error
  return data as Task[]
}

export async function getTaskById(id: string) {
  const { data, error } = await supabase
    .from("tasks")
    .select(taskFields)
    .eq("id", id)
    .single()

  if (error) throw error
  return data as Task
}

export async function createTask(userId: string, input: TaskInput) {
  const { data, error } = await supabase
    .from("tasks")
    .insert({ user_id: userId, ...input })
    .select(taskFields)
    .single()

  if (error) throw error
  return data as Task
}

export async function updateTask(id: string, input: TaskInput) {
  const { data, error } = await supabase
    .from("tasks")
    .update({ ...input, updated_at: new Date().toISOString() })
    .eq("id", id)
    .select(taskFields)
    .single()

  if (error) throw error
  return data as Task
}

export async function deleteTask(id: string) {
  const { error } = await supabase.from("tasks").delete().eq("id", id)
  if (error) throw error
}
