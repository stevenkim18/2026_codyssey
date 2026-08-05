import { Link, useParams } from "react-router"
import PageHeader from "../components/PageHeader"

function ProjectEditPage() {
  const { id } = useParams()

  return (
    <main className="mx-auto max-w-2xl px-6 py-10">
      <PageHeader eyebrow={`Project ${id ?? ""}`} title="프로젝트 수정" description="프로젝트 정보를 변경합니다." />
      <form className="space-y-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm" onSubmit={(event) => event.preventDefault()}>
        <label className="block text-sm font-medium text-slate-700">
          프로젝트 이름
          <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" defaultValue="새 프로젝트" required />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          설명
          <textarea className="mt-2 min-h-32 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" defaultValue="프로젝트 설명" />
        </label>
        <div className="flex justify-end gap-3">
          <Link className="rounded-xl border border-slate-300 px-4 py-3 font-semibold text-slate-700" to={`/projects/${id}`}>취소</Link>
          <button className="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700" type="submit">저장</button>
        </div>
      </form>
    </main>
  )
}

export default ProjectEditPage
