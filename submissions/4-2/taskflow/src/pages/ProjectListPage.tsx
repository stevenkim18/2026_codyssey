import { Link } from "react-router"
import EmptyState from "../components/EmptyState"
import PageHeader from "../components/PageHeader"

function ProjectListPage() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <PageHeader
        eyebrow="Projects"
        title="프로젝트"
        description="목표별로 할 일을 묶어 관리해보세요."
        action={<Link className="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700" to="/projects/new">새 프로젝트</Link>}
      />
      <EmptyState
        title="아직 프로젝트가 없습니다."
        description="첫 번째 프로젝트를 만들고 해야 할 일을 정리해보세요."
        action={<Link className="inline-flex rounded-xl bg-slate-900 px-4 py-3 font-semibold text-white hover:bg-slate-700" to="/projects/new">프로젝트 만들기</Link>}
      />
    </main>
  )
}

export default ProjectListPage
