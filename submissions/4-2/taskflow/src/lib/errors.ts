export function getErrorMessage(error: unknown) {
  if (error instanceof Error) {
    if (error.message.includes("Invalid login credentials")) {
      return "이메일 또는 비밀번호가 올바르지 않습니다."
    }

    if (error.message.includes("User already registered")) {
      return "이미 가입된 이메일입니다. 로그인해보세요."
    }

    return error.message
  }

  return "요청을 처리하지 못했습니다. 잠시 후 다시 시도해주세요."
}
