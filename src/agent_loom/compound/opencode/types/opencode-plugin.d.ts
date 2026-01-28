declare module "@opencode-ai/plugin" {
  export type Plugin = (ctx: {
    client: any;
    directory: string;
    worktree?: string;
    project?: any;
    $?: any;
  }) => Promise<any>;
  export const tool: any;
}
