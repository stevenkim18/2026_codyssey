import { Link } from "react-router"
import PageHeader from "../components/PageHeader"

const stats = [
  { label: "전체 프로젝트", value: "0" },
  { label: "전체 할 일", value: "0" },
  { label: "완료한 할 일", value: "0" },
]

function DashboardPage() {
  return (
    <main className="mx-auto max-w-6xl px-6 py-10">
      <PageHeader
        eyebrow="Overview"
        title="오늘의 작업을 확인하세요."
        description="프로젝트와 할 일의 진행 상황을 한눈에 확인하는 공간입니다."
        action={<Link className="rounded-xl bg-blue-600 px-4 py-3 font-semibold text-white hover:bg-blue-700" to="/projects/new">새 프로젝트</Link>}
      />
      <div className="grid gap-4 sm:grid-cols-3">
        {stats.map((stat) => (
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm" key={stat.label}>
            <p className="text-sm text-slate-500">{stat.label}</p>
            <p className="mt-3 text-3xl font-bold text-slate-950">{stat.value}</p>
          </div>
        ))}
      </div>
      <section className="mt-8 rounded-2xl border border-dashed border-slate-300 bg-white px-6 py-12 text-center">
        <h2 className="text-lg font-semibold text-slate-900">아직 등록된 할 일이 없습니다.</h2>
        <p className="mt-2 text-sm text-slate-500">프로젝트를 만들고 첫 번째 할 일을 추가해보세요.</p>
      </section>
    </main>
  )
}

export default DashboardPage
