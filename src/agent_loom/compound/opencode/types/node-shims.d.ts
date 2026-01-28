declare module "node:fs" { export const promises: any; }
declare module "node:path" { const x: any; export = x; }
declare module "node:child_process" { export const spawn: any; }
declare module "node:crypto" { export const randomUUID: any; }
declare const process: any;
