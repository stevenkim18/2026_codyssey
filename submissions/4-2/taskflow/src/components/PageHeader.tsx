import type { ReactNode } from "react"

type PageHeaderProps = {
  eyebrow?: string
  title: string
  description?: string
  action?: ReactNode
}

function PageHeader({ eyebrow, title, description, action }: PageHeaderProps) {
  return (
    <div className="mb-8 flex flex-col gap-5 sm:flex-row sm:items-end sm:justify-between">
      <div>
        {eyebrow && (
          <p className="mb-2 text-sm font-semibold uppercase tracking-widest text-blue-600">
            {eyebrow}
          </p>
        )}
        <h1 className="text-3xl font-bold tracking-tight text-slate-950">{title}</h1>
        {description && <p className="mt-2 max-w-2xl text-slate-500">{description}</p>}
      </div>
      {action}
    </div>
  )
}

export default PageHeader
