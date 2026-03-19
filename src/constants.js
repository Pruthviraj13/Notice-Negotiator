export const initialForm = {
  company_type: "service",
  notice_period: "30",
  offer_in_hand: "no",
  buyout_allowed: "no",
  project_critical: "medium",
  manager_type: "neutral",
  brutal_mode: false,
};

export const fieldGroups = [
  {
    label: "Company type",
    name: "company_type",
    options: [
      { value: "service", label: "Service" },
      { value: "startup", label: "Startup" },
      { value: "product", label: "Product" },
    ],
  },
  {
    label: "Notice period",
    name: "notice_period",
    options: [
      { value: "30", label: "30 days" },
      { value: "60", label: "60 days" },
      { value: "90", label: "90 days" },
    ],
  },
  {
    label: "Offer in hand",
    name: "offer_in_hand",
    options: [
      { value: "yes", label: "Yes" },
      { value: "no", label: "No" },
    ],
  },
  {
    label: "Buyout allowed",
    name: "buyout_allowed",
    options: [
      { value: "yes", label: "Yes" },
      { value: "no", label: "No" },
    ],
  },
  {
    label: "Project criticality",
    name: "project_critical",
    options: [
      { value: "low", label: "Low" },
      { value: "medium", label: "Medium" },
      { value: "high", label: "High" },
    ],
  },
  {
    label: "Manager type",
    name: "manager_type",
    options: [
      { value: "supportive", label: "Supportive" },
      { value: "neutral", label: "Neutral" },
      { value: "toxic", label: "Toxic" },
    ],
  },
];

export const strategyGroups = [
  { key: "safe", label: "Safe" },
  { key: "balanced", label: "Balanced" },
  { key: "aggressive", label: "Aggressive" },
];
