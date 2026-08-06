import { supabase } from "./supabase"
import type { Project, ProjectColor } from "../types/database"

const projectFields = "id,user_id,name,description,color,is_archived,created_at,updated_at"

export type ProjectInput = {
  name: string
  description: string | null
  color: ProjectColor
}

export async function getProjects(includeArchived = false) {
  let query = supabase
    .from("projects")
    .select(projectFields)
    .order("created_at", { ascending: false })

  if (!includeArchived) {
    query = query.eq("is_archived", false)
  }

  const { data, error } = await query
  if (error) throw error
  return data as Project[]
}

export async function getProjectById(id: string) {
  const { data, error } = await supabase
    .from("projects")
    .select(projectFields)
    .eq("id", id)
    .single()

  if (error) throw error
  return data as Project
}

export async function createProject(userId: string, input: ProjectInput) {
  const { data, error } = await supabase
    .from("projects")
    .insert({ user_id: userId, ...input })
    .select(projectFields)
    .single()

  if (error) throw error
  return data as Project
}

export async function updateProject(id: string, input: ProjectInput) {
  const { data, error } = await supabase
    .from("projects")
    .update({ ...input, updated_at: new Date().toISOString() })
    .eq("id", id)
    .select(projectFields)
    .single()

  if (error) throw error
  return data as Project
}

export async function deleteProject(id: string) {
  const { error } = await supabase
    .from("projects")
    .delete()
    .eq("id", id)

  if (error) throw error
}

export async function archiveProject(id: string) {
  const { error } = await supabase
    .from("projects")
    .update({ is_archived: true, updated_at: new Date().toISOString() })
    .eq("id", id)

  if (error) throw error
}
