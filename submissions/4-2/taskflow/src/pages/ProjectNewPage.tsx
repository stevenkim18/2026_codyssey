import { Link } from "react-router"
import PageHeader from "../components/PageHeader"

function ProjectNewPage() {
  return (
    <main className="mx-auto max-w-2xl px-6 py-10">
      <PageHeader eyebrow="Create" title="새 프로젝트" description="새 프로젝트의 기본 정보를 입력합니다." />
      <form className="space-y-5 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm" onSubmit={(event) => event.preventDefault()}>
        <label className="block text-sm font-medium text-slate-700">
          프로젝트 이름
          <input className="mt-2 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" required placeholder="예: Codyssey 4-2" />
        </label>
        <label className="block text-sm font-medium text-slate-700">
          설명
          <textarea className="mt-2 min-h-32 w-full rounded-xl border border-slate-300 px-4 py-3 outline-none focus:border-blue-500" placeholder="프로젝트 설명을 입력하세요." />
        </label>
        <div className="flex justify-end gap-3 pt-2">
          <Link className="rounded-xl border border-slate-300 px-4 py-3 font-semibold text-slate-700 hover:border-slate-400" to="/projects">취소</Link>
          <button className="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700" type="submit">저장</button>
        </div>
      </form>
    </main>
  )
}

export default ProjectNewPage
