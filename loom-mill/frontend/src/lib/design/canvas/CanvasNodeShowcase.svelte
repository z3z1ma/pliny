<script lang="ts">
  import { Svelvet } from 'svelvet';
  import InputNode from './InputNode.svelte';
  import ProcessingNode from './ProcessingNode.svelte';
  import QuestionNode from './QuestionNode.svelte';
  import ObservationNode from './ObservationNode.svelte';
  import OptionNode from './OptionNode.svelte';
  import RecordNode from './RecordNode.svelte';

  // Input Nodes
  let inputActive = { id: 'in-1', content: { text: 'I want to add a new API endpoint for user profiles.' }, status: 'active', parent_id: null };
  let inputStale = { id: 'in-2', content: { text: 'Wait, let me rephrase that.' }, status: 'stale', parent_id: 'in-1' };
  let inputDead = { id: 'in-3', content: { text: 'Nevermind, cancel that.' }, status: 'dead', parent_id: 'in-1' };

  // Processing Node
  let processing = { id: 'proc-1', content: { message: 'Exploring codebase...' } };

  // Question Nodes
  let qOpen = { id: 'q-1', content: { question: 'What fields should be included in the user profile?' }, status: 'active' };
  let qOptions = { id: 'q-2', content: { question: 'Should this be a public or private endpoint?', options: ['Public', 'Private (Auth required)'] }, status: 'active' };
  let qDead = { id: 'q-3', content: { question: 'Is this still relevant?' }, status: 'dead' };

  // Observation Nodes
  let obsActive = { id: 'obs-1', content: { observation: 'Found existing User model in src/models/user.ts' }, status: 'active' };
  let obsEvidence = { id: 'obs-2', content: { observation: 'The current API uses Express router.', evidence: 'import { Router } from "express";\nconst router = Router();' }, status: 'active' };

  // Option Nodes
  let opt1 = { id: 'opt-1', content: { label: 'Create new controller', description: 'Adds a dedicated controller for profiles' }, status: 'active', selected: false };
  let opt2 = { id: 'opt-2', content: { label: 'Extend existing user controller', description: 'Reuses the current user logic' }, status: 'active', selected: true };
  let optDead = { id: 'opt-3', content: { label: 'Use GraphQL', description: 'Migrate to GraphQL' }, status: 'dead', selected: false };

  // Record Nodes
  let recProposed = { id: 'rec-1', content: { surface: 'tickets', title: 'Add user profile API', body: '# Goal\nCreate a GET /api/users/:id/profile endpoint.\n\n# Scope\n- Add route\n- Add controller\n- Add tests' }, status: 'proposed' };
  let recAccepted = { id: 'rec-2', content: { surface: 'specs', title: 'User Profile Spec', body: 'The profile should contain:\n- id\n- name\n- avatar_url' }, status: 'accepted' };
  let recRejected = { id: 'rec-3', content: { surface: 'plans', title: 'Migration Plan', body: 'Step 1: Drop table...' }, status: 'rejected' };

  function handleRespond(text: string) {
    console.log('Responded:', text);
  }

  function handleSelect(id: string) {
    console.log('Selected option:', id);
  }

  function handleAccept(id: string) {
    console.log('Accepted record:', id);
  }

  function handleReject(id: string) {
    console.log('Rejected record:', id);
  }

  function handleEdit(id: string) {
    console.log('Edit record:', id);
  }
</script>

<div class="w-full h-full bg-bg-primary relative">
  <div class="absolute top-4 left-4 z-10 bg-bg-surface border border-border-default rounded px-3 py-2 text-[12px] text-text-primary shadow-md">
    <strong>Canvas Node Showcase</strong>
    <p class="text-text-tertiary mt-1">Testing all node types and states.</p>
  </div>

  <Svelvet width={2000} height={1500} minimap controls theme="dark">
    <!-- Input Nodes -->
    <InputNode node={inputActive} position={{ x: 100, y: 100 }} />
    <InputNode node={inputStale} position={{ x: 100, y: 250 }} />
    <InputNode node={inputDead} position={{ x: 100, y: 400 }} />

    <!-- Processing Node -->
    <ProcessingNode node={processing} position={{ x: 450, y: 100 }} />

    <!-- Question Nodes -->
    <QuestionNode node={qOpen} position={{ x: 700, y: 100 }} onRespond={handleRespond} />
    <QuestionNode node={qOptions} position={{ x: 700, y: 350 }} onRespond={handleRespond} />
    <QuestionNode node={qDead} position={{ x: 700, y: 600 }} onRespond={handleRespond} />

    <!-- Observation Nodes -->
    <ObservationNode node={obsActive} position={{ x: 1100, y: 100 }} />
    <ObservationNode node={obsEvidence} position={{ x: 1100, y: 250 }} />

    <!-- Option Nodes -->
    <OptionNode node={opt1} position={{ x: 1450, y: 100 }} onSelect={handleSelect} />
    <OptionNode node={opt2} position={{ x: 1450, y: 250 }} onSelect={handleSelect} />
    <OptionNode node={optDead} position={{ x: 1450, y: 400 }} onSelect={handleSelect} />

    <!-- Record Nodes -->
    <RecordNode node={recProposed} position={{ x: 1800, y: 100 }} onAccept={handleAccept} onReject={handleReject} onEdit={handleEdit} />
    <RecordNode node={recAccepted} position={{ x: 1800, y: 400 }} onAccept={handleAccept} onReject={handleReject} onEdit={handleEdit} />
    <RecordNode node={recRejected} position={{ x: 1800, y: 700 }} onAccept={handleAccept} onReject={handleReject} onEdit={handleEdit} />
  </Svelvet>
</div>
