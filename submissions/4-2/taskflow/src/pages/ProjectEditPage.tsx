import { useEffect, useState } from "react"
import { Link, useNavigate, useParams } from "react-router"
import PageHeader from "../components/PageHeader"
import { getErrorMessage } from "../lib/errors"
import { getProjectById, updateProject } from "../lib/projectApi"
import type { ProjectColor } from "../types/database"

const colors: { value: ProjectColor; label: string }[] = [
  { value: "blue", label: "파랑" },
  { value: "green", label: "초록" },
  { value: "yellow", label: "노랑" },
  { value: "red", label: "빨강" },
  { value: "purple", label: "보라" },
  { value: "gray", label: "회색" },
]

function ProjectEditPage() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [name, setName] = useState("")
  const [description, setDescription] = useState("")
  const [color, setColor] = useState<ProjectColor>("blue")
  const [isLoading, setIsLoading] = useState(true)
  const [isSubmitting, setIsSubmitting] = useState(false)
  const [error, setError] = useState("")

  useEffect(() => {
    if (!id) return
    const projectId = id
    let isMounted = true

    async function loadProject() {
      try {
        const project = await getProjectById(projectId)
        if (isMounted) {
          setName(project.name)
          setDescription(project.description ?? "")
          setColor(project.color as ProjectColor)
        }
      } catch (requestError) {
        if (isMounted) setError(getErrorMessage(requestError))
      } finally {
        if (isMounted) setIsLoading(false)
      }
    }

    void loadProject()
    return () => {
      isMounted = false
    }
  }, [id])

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!id) return
    setError("")
    if (!name.trim()) {
      setError("프로젝트 이름을 입력해주세요.")
      return
    }
    setIsSubmitting(true)

    try {
      await updateProject(id, {
        name: name.trim(),
        description: description.trim() || null,
        color,
      })
      navigate(`/projects/${id}`)
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="mx-auto max-w-2xl px-6 py-10">
      <PageHeader eyebrow={`Project ${id ?? ""}`} title="프로젝트 수정" description="프로젝트 정보를 변경합니다." />
      {isLoading ? <div className="rounded-2xl border border-slate-200 bg-white px-6 py-12 text-center text-sm text-slate-500">프로젝트를 불러오고 있습니다...</div> : <form className="space-y-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm" onSubmit={(event) => void handleSubmit(event)}>
        <label className="block text-sm font-medium text-slate-700">
          프로젝트 이름
          <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" value={name} onChange={(event) => setName(event.target.value)} required />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          설명
          <textarea className="mt-2 min-h-32 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" value={description} onChange={(event) => setDescription(event.target.value)} />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          색상
          <select className="mt-2 w-full rounded-xl border border-slate-300 bg-white px-4 py-3" value={color} onChange={(event) => setColor(event.target.value as ProjectColor)}>
            {colors.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
          </select>
        </label>
        {error && <p className="rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700" role="alert">{error}</p>}
        <div className="flex justify-end gap-3">
          <Link className="rounded-xl border border-slate-300 px-4 py-3 font-semibold text-slate-700" to={`/projects/${id}`}>취소</Link>
          <button className="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60" type="submit" disabled={isSubmitting}>{isSubmitting ? "저장 중..." : "저장"}</button>
        </div>
      </form>}
    </main>
  )
}

export default ProjectEditPage
