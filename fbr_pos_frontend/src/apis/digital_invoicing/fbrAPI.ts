import axiosInstance from '@/apis/axiosInstance'

export interface ClearScenariosResponse {
  message: string
  task_id: string
  scenarios: string[]
  note: string
}

export interface TaskStatusResponse {
  task_id: string
  status: 'PENDING' | 'STARTED' | 'SUCCESS' | 'FAILURE'
  result: any
}

class FbrAPI {
  // Trigger clear all scenarios
  async clearAllScenarios(companyId: number): Promise<ClearScenariosResponse> {
    const response = await axiosInstance.post(`/fbr/companies/${companyId}/clear-scenarios/`)
    return response.data
  }

  // Check task status
  async getTaskStatus(taskId: string): Promise<TaskStatusResponse> {
    const response = await axiosInstance.get(`/fbr/task-status/${taskId}/`)
    return response.data
  }

  // Get scenario logs
  async getScenarioLogs(companyId: number): Promise<any[]> {
    const response = await axiosInstance.get(`/fbr/companies/${companyId}/scenarios/logs/`)
    return response.data
  }

  // Get scenario templates
  async getScenarioTemplates(companyId: number): Promise<Record<string, any>> {
    const response = await axiosInstance.get(`/fbr/companies/${companyId}/scenarios/templates/`)
    return response.data
  }

  // Clear single scenario
  async clearSingleScenario(companyId: number, scenarioCode: string): Promise<any> {
    const response = await axiosInstance.post(`/fbr/companies/${companyId}/clear-scenario/`, {
      scenario_code: scenarioCode
    })
    return response.data
  }

  // Submit edited scenario
  async submitEditedScenario(companyId: number, scenarioCode: string, payload: any): Promise<any> {
    const response = await axiosInstance.post(`/fbr/companies/${companyId}/scenarios/submit-edited/`, {
      scenario_code: scenarioCode,
      payload: payload
    })
    return response.data
  }
}

export default new FbrAPI()
