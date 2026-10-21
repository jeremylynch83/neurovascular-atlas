import { Component, type ReactNode } from 'react';
import { reportStartupFailure } from './startup';

export class ViewerBoundary extends Component<{children: ReactNode}, {failed: boolean}> {
  state = {failed: false};
  static getDerivedStateFromError() { return {failed: true}; }
  componentDidCatch(error: Error) { reportStartupFailure(error); }
  render() { return this.state.failed ? null : this.props.children; }
}
