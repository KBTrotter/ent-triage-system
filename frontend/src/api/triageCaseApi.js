import apiClient from "./axios";

class TriageCaseApi {
  async getAllCases() {
    return apiClient.get('triage-cases/');
  }

  async getCaseById(id) {
    return apiClient.get(`/triage-cases/${id}`);
  }

  async createCase(caseData) {
    return apiClient.post('/triage-cases', caseData);
  }

  async updateCase(id, updateData) {
    return apiClient.put(`/triage-cases/${id}`, updateData);
  }

  async deleteCase(id) {
    return apiClient.delete(`/triage-cases/${id}`);
  }
}

export const triageCaseApi = new TriageCaseApi();
export default TriageCaseApi;