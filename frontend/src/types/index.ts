export type NotificationTheme = 'error' | 'secondary' | 'info' | 'success' | 'warn' | 'contrast'
export type TimeControl = 'blitz' | 'rapid' | 'bullet' | 'classical'

export interface PlatformOptions {
  name: string
  code: string
}

export interface OpeningData {
  total: number
  eco_codes: string[]
}
export interface GameData {
  count: number
  win_count: number
  draw_count: number
  loss_count: number
  opponents_avg_rating: Record<TimeControl, number>
  openings: [string, OpeningData][]
}
export interface RoastingUserData {
  tip: string
  roast: string
  encouragement: string
}
export interface AnalysisDataResult {
  file_upload?: string
  game?: GameData
  roasting_user?: RoastingUserData
  chess_style?: Object
}
export interface AnalysisData {
  result?: AnalysisDataResult
}
