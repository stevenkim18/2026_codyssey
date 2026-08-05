import { Link, useParams } from "react-router"
import PageHeader from "../components/PageHeader"

function ProjectDetailPage() {
  const { id } = useParams()

  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <PageHeader
        eyebrow={`Project ${id ?? ""}`}
        title="프로젝트 상세"
        description="이 프로젝트에 포함된 할 일을 관리합니다."
        action={<Link className="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700" to={`/projects/${id}/tasks/new`}>할 일 추가</Link>}
      />
      <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <p className="text-slate-500">아직 연결된 할 일이 없습니다.</p>
      </div>
    </main>
  )
}

export default ProjectDetailPage
