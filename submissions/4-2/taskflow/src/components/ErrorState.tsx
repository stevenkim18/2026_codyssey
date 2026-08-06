type ErrorStateProps = {
  message: string
  compact?: boolean
  onRetry?: () => void
}

function ErrorState({ message, compact = false, onRetry }: ErrorStateProps) {
  return (
    <div
      className={compact
        ? "rounded-xl bg-red-50 px-4 py-3 text-sm text-red-700"
        : "rounded-2xl border border-red-200 bg-red-50 px-6 py-8 text-center text-sm text-red-700"}
      role="alert"
    >
      <p>{message}</p>
      {onRetry && (
        <button
          className="mt-4 rounded-lg border border-red-300 px-3 py-2 font-semibold text-red-700 hover:border-red-400"
          type="button"
          onClick={onRetry}
        >
          다시 시도
        </button>
      )}
    </div>
  )
}

export default ErrorState
