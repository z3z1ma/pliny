export interface RecordMetadata {
  id: string | null;
  type: string | null;
  status: string | null;
  created: string | null;
  updated: string | null;
  risk: string | null;
  priority: string | null;
  depends_on: string[];
}

export type Heading = [number, string];

export interface LoomRecord {
  path: string;
  surface: string | null;
  metadata: RecordMetadata;
  headings: Heading[];
  references: string[];
  labeled_ids: string[];
}

export interface GitState {
  current_branch: string | null;
  recent_commits: string[];
  dirty: boolean;
}

export type WorkstationStatus = 'idle' | 'running' | 'paused' | 'stopped' | 'completed';

export interface OutputEvent {
  stream: string;
  data: string;
}

export interface WorkstationState {
  status: WorkstationStatus;
  worktree_path: string | null;
  process_id: number | null;
  exit_code: number | null;
  output: OutputEvent[];
}

export interface HarnessConfig {
  command: string;
  args: string[];
  env: Record<string, string>;
  cwd: string | null;
}

export interface MillState {
  records: LoomRecord[];
  git: GitState;
  workstations: Record<string, WorkstationState>;
}
