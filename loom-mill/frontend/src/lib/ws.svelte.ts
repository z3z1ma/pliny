import { type MillState, type LoomRecord, type GitState } from './types';

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

  private ws: WebSocket | null = null;

  connect() {
    if (this.ws) return;

    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    const host = window.location.hostname;
    // Assuming backend is on port 8765 as per dev.py
    const wsUrl = `${protocol}//${host}:8765/ws`;

    this.ws = new WebSocket(wsUrl);

    this.ws.onopen = () => {
      this.connected = true;
    };

    this.ws.onclose = () => {
      this.connected = false;
      this.ws = null;
      setTimeout(() => this.connect(), 2000);
    };

    this.ws.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    };
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
