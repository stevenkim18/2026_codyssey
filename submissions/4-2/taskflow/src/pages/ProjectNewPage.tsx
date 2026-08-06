import { useState } from "react"
import { Link, useNavigate } from "react-router"
import ErrorState from "../components/ErrorState"
import PageHeader from "../components/PageHeader"
import { useAuth } from "../contexts/useAuth"
import { getErrorMessage } from "../lib/errors"
import { createProject } from "../lib/projectApi"
import type { ProjectColor } from "../types/database"

const colors: { value: ProjectColor; label: string }[] = [
  { value: "blue", label: "파랑" },
  { value: "green", label: "초록" },
  { value: "yellow", label: "노랑" },
  { value: "red", label: "빨강" },
  { value: "purple", label: "보라" },
  { value: "gray", label: "회색" },
]

function ProjectNewPage() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [name, setName] = useState("")
  const [description, setDescription] = useState("")
  const [color, setColor] = useState<ProjectColor>("blue")
  const [error, setError] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    if (!user) return
    setError("")
    if (!name.trim()) {
      setError("프로젝트 이름을 입력해주세요.")
      return
    }
    setIsSubmitting(true)

    try {
      const project = await createProject(user.id, {
        name: name.trim(),
        description: description.trim() || null,
        color,
      })
      navigate(`/projects/${project.id}`)
    } catch (requestError) {
      setError(getErrorMessage(requestError))
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="mx-auto max-w-2xl px-6 py-10">
      <PageHeader eyebrow="Create" title="새 프로젝트" description="새 프로젝트의 기본 정보를 입력합니다." />
      <form className="space-y-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm" onSubmit={(event) => void handleSubmit(event)}>
        <label className="block text-sm font-medium text-slate-700">
          프로젝트 이름
          <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" required placeholder="예: Codyssey 4-2" value={name} onChange={(event) => setName(event.target.value)} />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          설명
          <textarea className="mt-2 min-h-32 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" placeholder="프로젝트 설명을 입력하세요." value={description} onChange={(event) => setDescription(event.target.value)} />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          색상
          <select className="mt-2 w-full rounded-xl border border-slate-300 bg-white px-4 py-3" value={color} onChange={(event) => setColor(event.target.value as ProjectColor)}>
            {colors.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
          </select>
        </label>
        {error && <ErrorState message={error} compact />}
        <div className="flex justify-end gap-3 pt-2">
          <Link className="rounded-xl border border-slate-300 px-4 py-3 font-semibold text-slate-700 hover:border-slate-400" to="/projects">취소</Link>
          <button className="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60" type="submit" disabled={isSubmitting}>{isSubmitting ? "저장 중..." : "저장"}</button>
        </div>
      </form>
    </main>
  )
}

export default ProjectNewPage
