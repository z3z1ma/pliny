import { type MillState, type LoomRecord, type GitState } from './types';
import { wsUrl } from './api';

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

  private ws: WebSocket | null = null;
  private reconnectTimeout: ReturnType<typeof setTimeout> | null = null;

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

    switch (type) {
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
    }
  }
}

export const store = new MillStore();
if (typeof window !== "undefined") (window as any).store = store;
