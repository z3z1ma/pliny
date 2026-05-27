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

export type WorkstationStatus = 'idle' | 'running' | 'paused' | 'stopped' | 'completed' | 'finished' | 'conflict';

export interface OutputEvent {
  stream: 'stdout' | 'stderr';
  line: string;
  timestamp: string;
}

export interface BackpressureSignal {
  kind: 'repeated_failure' | 'long_iteration' | 'no_record_change' | 'crash_loop';
  severity: 'alert' | 'warning';
  message: string;
  iteration_index: number;
  exit_code: number | null;
  duration_seconds: number | null;
  output_tail: string;
}

export interface AndonState {
  active: boolean;
  signals: BackpressureSignal[];
}

export interface FileChangeSummary {
  count: number;
  paths: string[];
  stat: string;
}

export interface ChangedRecord {
  path: string;
  record_id: string | null;
  changed_fields: string[];
}

export interface IterationSummary {
  label: string;
  ticket_slug: string;
  iteration: number;
  exit_code: number | null;
  duration_seconds: number;
  files_changed: FileChangeSummary;
  records_changed: ChangedRecord[];
  storage_path: string;
}

export interface IterationRecord {
  iteration: number;
  started_at: string;
  ended_at: string;
  duration_seconds: number;
  exit_code: number | null;
  commit_sha: string | null;
  files_changed: string[];
  lines_added: number;
  lines_removed: number;
  diff_stat: string;
  previous_commit_sha: string | null;
}

export interface TaktState {
  iteration: number;
  duration_seconds: number;
}

export interface WorkstationState {
  status: WorkstationStatus;
  ticket_id: string;
  ticket_slug: string;
  worktree_path: string | null;
  process_id: number | null;
  exit_code: number | null;
  output: OutputEvent[];
  iteration_summary: IterationSummary | null;
  backpressure_signals: BackpressureSignal[];
  andon: AndonState;
  takt?: TaktState;
}

export interface HarnessConfig {
  command: string;
  args: string[];
  env: Record<string, string>;
  cwd: string | null;
}

export interface AndonEventPayload {
  signal: 'alert' | 'stop';
  reasoning: string;
  patterns: string[];
  timestamp: string;
}

export interface ShippingEvent {
  ticket_id: string;
  action: 'merged' | 'conflict' | 'skipped' | 'aborted';
  target_branch: string;
  merge_sha: string | null;
  conflict_files: string[] | null;
  timestamp: string;
}

export interface InteractionBlock {
  id: string;
  type: string;
  timestamp: string;
  content: Record<string, any>;
}

export interface StagedRecord {
  temp_id: string;
  surface: string;
  title: string;
  content: string;
  branch: string;
  status: string;
  proposed_at: string;
  modified_at: string | null;
}

export interface MillState {
  records: LoomRecord[];
  git: GitState;
  workstations: Record<string, WorkstationState>;
  backpressure_signals: Record<string, BackpressureSignal[]>;
  shipping_events: ShippingEvent[];
  andon_events: Record<string, AndonEventPayload[]>;
}
