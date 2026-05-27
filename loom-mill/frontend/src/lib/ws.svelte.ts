import { type InteractionBlock, type MillState, type StagedRecord } from './types';
import { apiUrl, wsUrl } from './api';

export class MillStore {
  state = $state<MillState>({
    records: [],
    git: { current_branch: null, recent_commits: [], dirty: false },
    workstations: {},
    backpressure_signals: {},
    shipping_events: [],
    andon_events: {}
  });
  connected = $state(false);
  reconnecting = $state(false);
  reconnectAttempt = $state(0);
  error = $state<string | null>(null);
  maxReconnectAttempts = 10;

  chatSession = $state<{
    id: string | null;
    messages: Array<{ role: string; content: string; context?: any; timestamp: string }>;
    streaming: boolean;
    streamingContent: string;
    lastExitCode: number | null;
  }>({ id: null, messages: [], streaming: false, streamingContent: '', lastExitCode: null });

  shapingSession = $state<{
    id: string | null;
    phase: string;
    blocks: InteractionBlock[];
    stagedRecords: StagedRecord[];
    activeBranch: string;
    branches: string[];
    activeExplorations: string[];
  } | null>(null);

  private ws: WebSocket | null = null;
  private reconnectTimeout: ReturnType<typeof setTimeout> | null = null;
  private logHydrationRequests = new Set<string>();

  connect() {
    if (this.ws) return;

    const url = wsUrl('/ws');
    this.ws = new WebSocket(url);

    this.ws.onopen = () => {
      this.connected = true;
      this.reconnecting = false;
      this.reconnectAttempt = 0;
      this.error = null;
    };

    this.ws.onclose = () => {
      this.connected = false;
      this.ws = null;
      
      if (this.reconnectAttempt < this.maxReconnectAttempts) {
        this.reconnecting = true;
        const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempt), 16000);
        this.reconnectAttempt++;
        this.reconnectTimeout = setTimeout(() => this.connect(), delay);
      } else {
        this.reconnecting = false;
        this.error = 'Connection lost. Max reconnect attempts reached.';
      }
    };

    this.ws.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        this.handleMessage(message);
      } catch (err) {
        console.error('Failed to parse WebSocket message:', err, event.data);
      }
    };
  }

  retry() {
    this.reconnectAttempt = 0;
    this.error = null;
    if (this.reconnectTimeout) {
      clearTimeout(this.reconnectTimeout);
      this.reconnectTimeout = null;
    }
    this.connect();
  }

  clearAndonEvents(workstationId: string) {
    if (this.state.andon_events[workstationId]) {
      this.state.andon_events[workstationId] = [];
    }
  }

  async hydrateWorkstationLogs(workstationId: string) {
    const workstation = this.state.workstations[workstationId];
    if (!workstation || workstation.output?.length || this.logHydrationRequests.has(workstationId)) return;

    this.logHydrationRequests.add(workstationId);
    try {
      const response = await fetch(apiUrl(`/workstations/${workstationId}/logs?stream=stdout&tail=500`));
      if (!response.ok) return;
      const data = await response.json();
      const lines = Array.isArray(data.lines) ? data.lines : [];
      const current = this.state.workstations[workstationId];
      if (!current || current.output?.length) return;
      current.output = lines.map((line: string) => ({ stream: 'stdout', line, timestamp: '' }));
    } catch (err) {
      console.error('Failed to hydrate workstation logs:', err);
    } finally {
      this.logHydrationRequests.delete(workstationId);
    }
  }

  private handleMessage(message: any) {
    const { type, data, workstation_id, event, payload } = message;

    if (event && workstation_id) {
      // Handle workstation events
      if (!this.state.workstations[workstation_id] && event !== 'state_change') {
        return; // Ignore events for unknown workstations unless it's a state_change
      }

      switch (event) {
        case 'state_change':
          this.state.workstations[workstation_id] = payload;
          if (payload.backpressure_signals?.length) {
            this.state.backpressure_signals[workstation_id] = payload.backpressure_signals;
          } else {
            delete this.state.backpressure_signals[workstation_id];
          }
          break;
        case 'removed':
          delete this.state.workstations[workstation_id];
          delete this.state.backpressure_signals[workstation_id];
          break;
        case 'log':
          if (!this.state.workstations[workstation_id].output) {
            this.state.workstations[workstation_id].output = [];
          }
          this.state.workstations[workstation_id].output.push(payload);
          // Keep last 500 lines
          if (this.state.workstations[workstation_id].output.length > 500) {
            this.state.workstations[workstation_id].output.shift();
          }
          break;
        case 'iteration':
          this.state.workstations[workstation_id].iteration_summary = payload;
          break;
        case 'takt':
          this.state.workstations[workstation_id].takt = payload;
          break;
        case 'andon':
          if (!this.state.andon_events[workstation_id]) {
            this.state.andon_events[workstation_id] = [];
          }
          this.state.andon_events[workstation_id].push({
            ...payload,
            timestamp: new Date().toISOString()
          });
          break;
        case 'shipping':
          this.state.shipping_events.unshift(payload);
          break;
      }
      return;
    }

    const eventType = type || event;
    switch (eventType) {
      case 'snapshot':
        this.state.records = data.records;
        this.state.git = data.git;
        this.state.workstations = data.workstations || {};
        this.state.backpressure_signals = data.backpressure_signals || {};
        this.state.shipping_events = data.shipping_events || [];
        this.state.andon_events = data.andon_events || {};
        break;
      case 'RecordAdded':
        this.state.records.push(data.record);
        break;
      case 'RecordChanged':
        const index = this.state.records.findIndex(r => r.path === data.record.path);
        if (index !== -1) {
          this.state.records[index] = data.record;
        } else {
          this.state.records.push(data.record);
        }
        break;
      case 'RecordRemoved':
        this.state.records = this.state.records.filter(r => r.path !== data.path);
        break;
      case 'GitStateChanged':
        this.state.git = data.git;
        break;
      case 'chat_stream':
        if (data.session_id === this.chatSession.id) {
          this.chatSession = {
            ...this.chatSession,
            streaming: true,
            streamingContent: this.chatSession.streamingContent + data.delta
          };
        }
        break;
      case 'chat_complete':
        if (data.session_id === this.chatSession.id) {
          this.chatSession = {
            ...this.chatSession,
            streaming: false,
            lastExitCode: data.exit_code ?? null,
            messages: [...this.chatSession.messages, data.message],
            streamingContent: ''
          };
        }
        break;
      case 'chat_error':
        if (data.session_id === this.chatSession.id) {
          this.chatSession = {
            ...this.chatSession,
            streaming: false,
            lastExitCode: null,
            messages: [...this.chatSession.messages, { role: 'system', content: `Error: ${data.error}`, timestamp: new Date().toISOString() }],
            streamingContent: ''
          };
        }
        break;
      case 'shaping:block_added':
        this.ensureShapingSession(data.session_id);
        this.shapingSession!.blocks = [...this.shapingSession!.blocks, data.block];
        break;
      case 'shaping:phase_changed':
        this.ensureShapingSession(data.session_id);
        this.shapingSession!.phase = data.phase;
        break;
      case 'shaping:session_ended':
        if (this.shapingSession?.id === data.session_id) {
          this.shapingSession = null;
        }
        break;
    }
  }

  private ensureShapingSession(sessionId: string) {
    if (this.shapingSession?.id === sessionId) return;
    this.shapingSession = {
      id: sessionId,
      phase: 'exploring',
      blocks: [],
      stagedRecords: [],
      activeBranch: 'main',
      branches: ['main'],
      activeExplorations: []
    };
  }
}

export const store = new MillStore();
if (typeof window !== "undefined") (window as any).store = store;
