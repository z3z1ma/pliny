export interface LayoutNode {
  id: string;
  parent_id: string | null;
  position: { x: number; y: number } | null;
  status?: string;
}

export interface LayoutResult {
  positions: Record<string, { x: number; y: number }>;
}

const NODE_WIDTH = 280;
const H_GAP = 48;
const V_GAP = 150;
const Y_OFFSET = 50;
const X_ORIGIN = 400;

export function computeTreeLayout(nodes: LayoutNode[], _edges: any[]): LayoutResult {
  const positions: Record<string, { x: number; y: number }> = {};
  const childrenMap: Record<string, string[]> = {};
  const nodeMap: Record<string, LayoutNode> = {};

  nodes.forEach((n) => {
    nodeMap[n.id] = n;
    childrenMap[n.id] = [];
  });

  const roots: string[] = [];
  nodes.forEach((n) => {
    if (n.parent_id && nodeMap[n.parent_id]) {
      childrenMap[n.parent_id].push(n.id);
    } else {
      roots.push(n.id);
    }
  });

  const depths: Record<string, number> = {};
  function assignDepth(nodeId: string, depth: number) {
    depths[nodeId] = depth;
    childrenMap[nodeId].forEach((c) => assignDepth(c, depth + 1));
  }
  roots.forEach((r) => assignDepth(r, 0));

  // Post-order X assignment with a single advancing cursor for leaves.
  // Each subtree occupies a contiguous horizontal band, so siblings never overlap.
  let cursor = 0;
  const slot = NODE_WIDTH + H_GAP;

  function assignX(nodeId: string): number {
    const children = childrenMap[nodeId];
    let x: number;
    if (children.length === 0) {
      x = cursor;
      cursor += slot;
    } else {
      const childXs = children.map((c) => assignX(c));
      x = (childXs[0] + childXs[childXs.length - 1]) / 2;
    }
    positions[nodeId] = { x, y: depths[nodeId] * V_GAP + Y_OFFSET };
    return x;
  }

  roots.forEach((r) => {
    assignX(r);
    cursor += slot; // gap between separate root trees
  });

  // Honor pinned (manually dragged) positions: override after layout.
  nodes.forEach((n) => {
    if (n.position) {
      positions[n.id] = { x: n.position.x, y: n.position.y };
    }
  });

  // Shift the whole (unpinned) graph so the first root sits at X_ORIGIN.
  if (roots.length > 0 && !nodeMap[roots[0]].position) {
    const shift = X_ORIGIN - positions[roots[0]].x;
    nodes.forEach((n) => {
      if (!n.position) positions[n.id].x += shift;
    });
  }

  return { positions };
}
