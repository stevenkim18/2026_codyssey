import { createProject } from "./projectApi"
import { createTask } from "./taskApi"
import type { ProjectColor, TaskPriority, TaskStatus } from "../types/database"

type DemoProject = {
  name: string
  description: string
  color: ProjectColor
  tasks: {
    title: string
    description: string
    status: TaskStatus
    priority: TaskPriority
    dueDateOffset: number
  }[]
}

const demoProjects: DemoProject[] = [
  {
    name: "Codyssey 4-2 과제",
    description: "React와 Supabase로 TaskFlow를 완성하는 학습 프로젝트입니다.",
    color: "blue",
    tasks: [
      { title: "Supabase RLS 정책 점검하기", description: "프로젝트와 할 일의 사용자별 접근 정책을 확인합니다.", status: "done", priority: "high", dueDateOffset: -2 },
      { title: "대시보드 화면 다듬기", description: "통계 카드와 최근 할 일 목록의 정보를 정리합니다.", status: "in_progress", priority: "medium", dueDateOffset: 1 },
      { title: "최종 배포 준비하기", description: "환경변수와 배포 설정을 점검합니다.", status: "todo", priority: "high", dueDateOffset: 5 },
    ],
  },
  {
    name: "개인 학습 루틴",
    description: "매일 조금씩 꾸준히 진행할 공부와 복습을 관리합니다.",
    color: "green",
    tasks: [
      { title: "TypeScript 타입 좁히기 복습", description: "유니언 타입과 타입 가드를 예제로 복습합니다.", status: "done", priority: "low", dueDateOffset: -1 },
      { title: "React Hooks 정리", description: "useEffect와 커스텀 훅의 사용 기준을 정리합니다.", status: "in_progress", priority: "medium", dueDateOffset: 2 },
    ],
  },
  {
    name: "TaskFlow 개선 아이디어",
    description: "MVP 이후 추가할 수 있는 기능을 모아두는 프로젝트입니다.",
    color: "purple",
    tasks: [
      { title: "상태별 필터 추가 검토", description: "todo, 진행 중, 완료 상태별 필터의 사용성을 확인합니다.", status: "todo", priority: "medium", dueDateOffset: 7 },
      { title: "다크 모드 조사", description: "Tailwind CSS 기반 다크 모드 적용 방법을 조사합니다.", status: "todo", priority: "low", dueDateOffset: 10 },
    ],
  },
]

export const demoProjectNames = demoProjects.map((project) => project.name)

function dateFromToday(offset: number) {
  const date = new Date()
  date.setDate(date.getDate() + offset)
  return date.toISOString().slice(0, 10)
}

export async function createDemoData(userId: string) {
  let projectCount = 0
  let taskCount = 0

  for (const demoProject of demoProjects) {
    const project = await createProject(userId, {
      name: demoProject.name,
      description: demoProject.description,
      color: demoProject.color,
    })
    projectCount += 1

    for (const demoTask of demoProject.tasks) {
      await createTask(userId, {
        project_id: project.id,
        title: demoTask.title,
        description: demoTask.description,
        status: demoTask.status,
        priority: demoTask.priority,
        due_date: dateFromToday(demoTask.dueDateOffset),
      })
      taskCount += 1
    }
  }

  return { projectCount, taskCount }
}
