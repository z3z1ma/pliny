import { type MillState, type LoomRecord, type GitState } from './types';

export class MillStore {
  state = $state<MillState>({
    records: [],
    git: { current_branch: null, recent_commits: [], dirty: false },
    workstations: {}
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
    const { type, data } = message;

    switch (type) {
      case 'snapshot':
        this.state.records = data.records;
        this.state.git = data.git;
        this.state.workstations = data.workstations || {};
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
      case 'WorkstationStateChanged':
        this.state.workstations[data.ticket_id] = data.workstation;
        break;
    }
  }
}

export const store = new MillStore();
