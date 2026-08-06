type LoadingStateProps = {
  message?: string
  fullPage?: boolean
}

function LoadingState({ message = "데이터를 불러오고 있습니다...", fullPage = false }: LoadingStateProps) {
  return (
    <div
      className={fullPage
        ? "flex min-h-[calc(100vh-73px)] items-center justify-center text-sm text-slate-500"
        : "rounded-2xl border border-slate-200 bg-white px-6 py-12 text-center text-sm text-slate-500"}
      role="status"
      aria-live="polite"
    >
      {message}
    </div>
  )
}

export default LoadingState
