export type RootStackParamList = {
  Login:          undefined;
  Signup:         undefined;
  ForgotPassword: undefined;
  ResetPassword:  { token?: string };
  Main:           undefined;
};

export type MainTabParamList = {
  Dashboard: undefined;
  Upload:    undefined;
  History:   undefined;
  Results:   { scanId?: number };
  Profile:   undefined;
};

export type MainStackParamList = {
  Tabs:     undefined;
  Workflow: undefined;
};
