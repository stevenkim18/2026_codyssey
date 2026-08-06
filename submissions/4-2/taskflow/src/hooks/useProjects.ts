import { useCallback, useEffect, useState } from "react"
import type { Project, Task } from "../types/database"
import { getProjects } from "../lib/projectApi"
import { getTasks } from "../lib/taskApi"
import { getErrorMessage } from "../lib/errors"

type UseProjectsResult = {
  projects: Project[]
  tasks: Task[]
  isLoading: boolean
  error: string
  reload: () => void
}

export function useProjects(userId?: string): UseProjectsResult {
  const [projects, setProjects] = useState<Project[]>([])
  const [tasks, setTasks] = useState<Task[]>([])
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState("")
  const [reloadToken, setReloadToken] = useState(0)

  const reload = useCallback(() => {
    setReloadToken((token) => token + 1)
  }, [])

  useEffect(() => {
    if (!userId) return

    let isMounted = true

    async function loadProjects() {
      setIsLoading(true)
      setError("")

      try {
        const [projectData, taskData] = await Promise.all([getProjects(), getTasks()])
        if (isMounted) {
          setProjects(projectData)
          setTasks(taskData)
        }
      } catch (requestError) {
        if (isMounted) setError(getErrorMessage(requestError))
      } finally {
        if (isMounted) setIsLoading(false)
      }
    }

    void loadProjects()
    return () => {
      isMounted = false
    }
  }, [reloadToken, userId])

  return {
    projects: userId ? projects : [],
    tasks: userId ? tasks : [],
    isLoading: userId ? isLoading : false,
    error: userId ? error : "",
    reload,
  }
}
