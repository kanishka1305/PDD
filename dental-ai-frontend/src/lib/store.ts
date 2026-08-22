export interface User {
  id: number
  name: string
  email: string
}

export interface AnalysisResult {
  scan_id: number
  status: string
  analysis: {
    volume_shape: number[]
    detected_voxels: number
    estimated_volume: number
    segmentation_image: string
    stl_file: string
    bone_volume: number
    cortical_bone: number
    trabecular_bone: number
    nerve_canal_volume: number
    nerve_distance: string
    nerve_distance_value: number
    bone_loss: number
    confidence: number
    report_id: string
    report_date: string
    condylar_head_l_volume: number
    condylar_head_r_volume: number
    coronoid_l_volume: number
    coronoid_r_volume: number
    angle_ramus_l_volume: number
    angle_ramus_r_volume: number
    body_l_volume: number
    body_r_volume: number
    symphyseal_parasymphyseal_volume: number
    report_path: string
  }
}

const KEY_USER   = 'dental_user'
const KEY_RESULT = 'dental_last_result'

export const store = {
  getUser: (): User | null => { try { return JSON.parse(localStorage.getItem(KEY_USER) || 'null') } catch { return null } },
  setUser: (u: User) => localStorage.setItem(KEY_USER, JSON.stringify(u)),
  clearUser: () => localStorage.removeItem(KEY_USER),
  getResult: (): AnalysisResult | null => { try { return JSON.parse(localStorage.getItem(KEY_RESULT) || 'null') } catch { return null } },
  setResult: (r: AnalysisResult) => localStorage.setItem(KEY_RESULT, JSON.stringify(r)),
  clear: () => localStorage.clear(),
}
