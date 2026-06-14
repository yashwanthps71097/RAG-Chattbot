import React, { useState } from 'react';

const API_URL = window.location.port === '5173' ? 'http://localhost:8000/api/chat' : '/api/chat';

function App() {
  const [view, setView] = useState('landing'); // 'landing', 'loading', 'answer', 'refusal'
  const [query, setQuery] = useState('');
  const [activeQuery, setActiveQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);
  const [verifyOpen, setVerifyOpen] = useState(false);
  
  const [answerData, setAnswerData] = useState({
    answer: '',
    citation_url: '',
    last_updated: '',
    is_refusal: false,
    disclaimer: '',
    source_chunks: []
  });

  const handleSearch = async (searchQuery) => {
    const q = searchQuery || query;
    if (!q.trim()) return;

    setActiveQuery(q);
    setView('loading');
    setLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: q })
      });

      if (!response.ok) {
        throw new Error('Failed to get response from server.');
      }

      const data = await response.json();
      setAnswerData({
        answer: data.answer || '',
        citation_url: data.citation_url || 'https://www.amfiindia.com/investor-corner/educational-material.html',
        last_updated: data.last_updated || new Date().toLocaleDateString(),
        is_refusal: data.is_refusal || false,
        disclaimer: data.disclaimer || 'Facts-only. No investment advice.',
        source_chunks: data.source_chunks || []
      });

      if (data.is_refusal) {
        setView('refusal');
      } else {
        setView('answer');
      }
    } catch (error) {
      console.error(error);
      setAnswerData({
        answer: 'An error occurred while connecting to the assistant service. Please check your backend is running.',
        citation_url: 'https://www.amfiindia.com/investor-corner/educational-material.html',
        last_updated: new Date().toLocaleDateString(),
        is_refusal: true,
        disclaimer: 'Connection Error',
        source_chunks: []
      });
      setView('refusal');
    } finally {
      setLoading(false);
    }
  };

  const handleSuggest = (suggestion) => {
    setQuery(suggestion);
    handleSearch(suggestion);
  };

  const handleCopy = () => {
    navigator.clipboard.writeText(answerData.answer);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const getSourceDisplay = (url) => {
    try {
      const parsed = new URL(url);
      if (parsed.hostname.includes('groww.in')) {
        const paths = parsed.pathname.split('/').filter(Boolean);
        const name = paths[paths.length - 1];
        return name
          .split('-')
          .map(w => w.charAt(0).toUpperCase() + w.slice(1))
          .join(' ') + ' Page';
      }
      if (parsed.hostname.includes('amfiindia')) {
        return 'AMFI Investor Corner';
      }
      return parsed.hostname;
    } catch {
      return 'Official Document Sources';
    }
  };

  return (
    <>
      {/* TopAppBar */}
      <header className="bg-surface docked full-width top-0 border-b border-outline-variant z-50">
        <div className="flex justify-between items-center px-lg py-md w-full max-w-max-width-desktop mx-auto">
          <div 
            className="flex items-center gap-sm cursor-pointer active:opacity-80"
            onClick={() => { setView('landing'); setQuery(''); }}
          >
            <span className="material-symbols-outlined text-primary text-headline-md" data-icon="account_balance">account_balance</span>
            <h1 className="font-headline-md text-headline-md font-bold text-primary">Mutual Fund FAQ Assistant</h1>
          </div>
          <div className="hidden md:flex items-center gap-lg">
            <span 
              onClick={() => { setView('landing'); setQuery(''); }}
              className={`cursor-pointer py-xs text-label-md font-bold ${view === 'landing' ? 'text-primary border-b-2 border-primary' : 'text-on-surface-variant hover:bg-surface-container-low px-sm rounded'}`}
            >
              Home
            </span>
            <div className="px-md py-sm bg-primary-container text-on-primary-container rounded-full text-label-md font-label-md flex items-center gap-xs">
              <span className="material-symbols-outlined text-[18px] font-fill" data-icon="verified" style={{ fontVariationSettings: "'FILL' 1" }}>verified</span>
              Facts-Only Information
            </div>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-grow flex flex-col justify-start">
        {/* Landing View */}
        {view === 'landing' && (
          <>
            <section className="relative pt-3xl pb-2xl overflow-hidden">
              <div className="max-w-max-width-desktop mx-auto px-margin-mobile md:px-lg relative z-10 text-center">
                <div className="inline-flex items-center gap-sm bg-tertiary-container/10 border border-tertiary-container/30 px-md py-xs rounded-full text-tertiary font-label-md mb-lg mx-auto">
                  <span className="material-symbols-outlined text-[18px]" data-icon="info">info</span>
                  Facts-only. No investment advice.
                </div>
                <h2 className="font-display-lg text-display-lg text-on-background mb-md max-w-3xl mx-auto">
                  Get Verified Mutual Fund Information
                </h2>
                <p className="font-body-lg text-body-lg text-on-surface-variant mb-2xl max-w-2xl mx-auto">
                  Answers sourced exclusively from official HDFC Scheme Information Documents (SID) on Groww. No marketing fluff, just regulatory data.
                </p>

                {/* Conversational Search Area */}
                <div className="max-w-3xl mx-auto relative group mb-xl">
                  <div className="absolute -inset-1 bg-gradient-to-r from-primary to-secondary rounded-xl blur opacity-25 group-focus-within:opacity-50 transition duration-1000"></div>
                  <form 
                    onSubmit={(e) => { e.preventDefault(); handleSearch(); }}
                    className="relative bg-surface-container-lowest border border-outline-variant rounded-xl p-base flex items-center shadow-lg transition-all duration-300 focus-within:ring-2 focus-within:ring-primary/20"
                  >
                    <span className="material-symbols-outlined ml-md text-outline" data-icon="search">search</span>
                    <input 
                      className="w-full bg-transparent border-none focus:ring-0 px-md py-xl font-body-md text-on-surface placeholder:text-on-surface-variant/60 outline-none" 
                      placeholder="Ask about expense ratio, exit load, SIP amount for HDFC Funds..." 
                      type="text"
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                    />
                    <button 
                      type="submit"
                      className="mr-base bg-primary text-on-primary px-xl py-md rounded-lg font-label-md hover:brightness-110 transition-all flex items-center gap-sm"
                    >
                      Verify 
                      <span className="material-symbols-outlined text-[18px]" data-icon="arrow_forward">arrow_forward</span>
                    </button>
                  </form>
                </div>

                {/* Suggestion Buttons */}
                <div className="mt-xl flex flex-wrap justify-center gap-md">
                  <button 
                    onClick={() => handleSuggest('What is the exit load of HDFC Small Cap Fund?')}
                    className="bg-surface border border-outline-variant hover:border-primary hover:text-primary transition-all px-md py-sm rounded-full text-body-sm text-on-surface-variant flex items-center gap-xs"
                  >
                    <span className="material-symbols-outlined text-[16px]" data-icon="chat_bubble">chat_bubble</span>
                    "What is the exit load of HDFC Small Cap Fund?"
                  </button>
                  <button 
                    onClick={() => handleSuggest('Who manages the HDFC Defence Fund?')}
                    className="bg-surface border border-outline-variant hover:border-primary hover:text-primary transition-all px-md py-sm rounded-full text-body-sm text-on-surface-variant flex items-center gap-xs"
                  >
                    <span className="material-symbols-outlined text-[16px]" data-icon="chat_bubble">chat_bubble</span>
                    "Who manages the HDFC Defence Fund?"
                  </button>
                  <button 
                    onClick={() => handleSuggest('What is the minimum SIP for HDFC Mid-Cap Fund?')}
                    className="bg-surface border border-outline-variant hover:border-primary hover:text-primary transition-all px-md py-sm rounded-full text-body-sm text-on-surface-variant flex items-center gap-xs"
                  >
                    <span className="material-symbols-outlined text-[16px]" data-icon="chat_bubble">chat_bubble</span>
                    "What is the minimum SIP for HDFC Mid-Cap?"
                  </button>
                </div>
              </div>
            </section>

            {/* Privacy Banner */}
            <section className="bg-primary-container text-on-primary-container py-md w-full">
              <div className="max-w-max-width-desktop mx-auto px-margin-mobile md:px-lg flex items-center justify-center gap-md text-center">
                <span className="material-symbols-outlined" data-icon="lock" style={{ fontVariationSettings: "'FILL' 1" }}>lock</span>
                <p className="font-label-md text-label-md">
                  We do not collect PAN, Aadhaar, account numbers, OTPs, phone numbers, or email addresses.
                </p>
              </div>
            </section>

            {/* Supported Topics (Bento Grid) */}
            <section className="py-3xl bg-surface w-full">
              <div className="max-w-max-width-desktop mx-auto px-margin-mobile md:px-lg">
                <div className="mb-2xl text-center">
                  <h3 class="font-headline-lg text-headline-lg text-on-surface mb-sm">Comprehensive Regulatory Data</h3>
                  <p class="font-body-md text-body-md text-on-surface-variant">Instant access to facts usually hidden in lengthy scheme documents.</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-lg">
                  {/* Cards */}
                  <div className="bg-surface-container-low border border-outline-variant rounded-xl p-xl hover:shadow-md transition-all group">
                    <div className="w-12 h-12 rounded-lg bg-primary/10 text-primary flex items-center justify-center mb-md group-hover:bg-primary group-hover:text-on-primary transition-colors">
                      <span className="material-symbols-outlined" data-icon="payments">payments</span>
                    </div>
                    <h4 className="font-headline-md text-headline-md text-on-surface mb-sm">Expense Ratio</h4>
                    <p className="font-body-sm text-body-sm text-on-surface-variant">Daily updated Total Expense Ratio (TER) as reported in mutual fund scheme information sheets.</p>
                  </div>
                  <div className="bg-surface-container-low border border-outline-variant rounded-xl p-xl hover:shadow-md transition-all group">
                    <div className="w-12 h-12 rounded-lg bg-primary/10 text-primary flex items-center justify-center mb-md group-hover:bg-primary group-hover:text-on-primary transition-colors">
                      <span className="material-symbols-outlined" data-icon="logout">logout</span>
                    </div>
                    <h4 className="font-headline-md text-headline-md text-on-surface mb-sm">Exit Load</h4>
                    <p className="font-body-sm text-body-sm text-on-surface-variant">Clarity on redemption penalties and lock-in intervals based on the holding durations.</p>
                  </div>
                  <div className="bg-surface-container-low border border-outline-variant rounded-xl p-xl hover:shadow-md transition-all group">
                    <div className="w-12 h-12 rounded-lg bg-primary/10 text-primary flex items-center justify-center mb-md group-hover:bg-primary group-hover:text-on-primary transition-colors">
                      <span className="material-symbols-outlined" data-icon="speed">speed</span>
                    </div>
                    <h4 className="font-headline-md text-headline-md text-on-surface mb-sm">Riskometer</h4>
                    <p className="font-body-sm text-body-sm text-on-surface-variant">Visual risk categorization assigned to schemes in accordance with SEBI guidelines.</p>
                  </div>
                </div>
              </div>
            </section>

            {/* Trust Section */}
            <section className="py-3xl bg-surface-container-lowest w-full">
              <div className="max-w-max-width-desktop mx-auto px-margin-mobile md:px-lg">
                <div className="flex flex-col lg:flex-row items-center gap-3xl">
                  <div className="lg:w-1/2">
                    <div className="inline-flex items-center gap-xs text-secondary font-label-md mb-md">
                      <span className="material-symbols-outlined text-[20px]" data-icon="shield" style={{ fontVariationSettings: "'FILL' 1" }}>shield</span>
                      Built on Trust &amp; Integrity
                    </div>
                    <h3 className="font-headline-lg text-headline-lg text-on-surface mb-lg">A Research Tool Designed for Modern Investors</h3>
                    <div className="space-y-xl">
                      <div className="flex gap-md">
                        <div className="flex-shrink-0 mt-xs">
                          <span className="material-symbols-outlined text-secondary" data-icon="source">source</span>
                        </div>
                        <div>
                          <h5 className="font-headline-md text-headline-md text-on-surface mb-xs">Official Sources Only</h5>
                          <p className="font-body-md text-body-md text-on-surface-variant">We index only official Groww pages and direct Scheme Information Documents (SIDs).</p>
                        </div>
                      </div>
                      <div className="flex gap-md">
                        <div className="flex-shrink-0 mt-xs">
                          <span className="material-symbols-outlined text-secondary" data-icon="no_accounts">no_accounts</span>
                        </div>
                        <div>
                          <h5 className="font-headline-md text-headline-md text-on-surface mb-xs">No Personal Data Collection</h5>
                          <p className="font-body-md text-body-md text-on-surface-variant">Browse completely anonymously. No account creation or PII required.</p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="lg:w-1/2 relative">
                    <div className="aspect-square bg-surface-container rounded-3xl overflow-hidden relative border border-outline-variant shadow-2xl">
                      <img 
                        className="w-full h-full object-cover grayscale contrast-125 opacity-40" 
                        alt="Financial details concept"
                        src="https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?q=80&w=600&auto=format&fit=crop"
                      />
                      <div className="absolute inset-0 bg-gradient-to-tr from-primary/20 to-transparent"></div>
                      <div className="absolute bottom-lg left-lg right-lg bg-surface/90 backdrop-blur-md p-lg rounded-xl border border-white/20 shadow-lg">
                        <div className="flex items-center gap-sm mb-sm">
                          <span className="material-symbols-outlined text-primary" data-icon="check_circle" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
                          <span className="font-label-md text-primary">Compliance Verified</span>
                        </div>
                        <p className="font-body-sm text-on-surface italic">"The facts provided align precisely with current SEBI compliance and AMFI reports."</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </>
        )}

        {/* Loading View */}
        {view === 'loading' && (
          <section className="flex-grow flex flex-col items-center justify-center py-3xl px-lg">
            <div className="animate-spin rounded-full h-12 w-12 border-4 border-primary border-t-transparent mb-lg"></div>
            <p className="text-body-lg text-on-surface-variant animate-pulse">
              Consulting regulatory documents for "{activeQuery}"...
            </p>
          </section>
        )}

        {/* Answer View */}
        {view === 'answer' && (
          <div className="w-full max-w-max-width-desktop mx-auto px-lg py-3xl">
            {/* Search header area */}
            <div className="max-w-3xl mx-auto mb-2xl">
              <form 
                onSubmit={(e) => { e.preventDefault(); handleSearch(); }}
                className="relative group"
              >
                <div className="absolute inset-y-0 left-0 pl-md flex items-center pointer-events-none">
                  <span className="material-symbols-outlined text-outline" data-icon="search">search</span>
                </div>
                <input 
                  className="block w-full pl-xl pr-32 py-xl border border-outline-variant bg-surface-container-lowest rounded-xl text-body-lg focus:ring-2 focus:ring-primary focus:border-primary shadow-sm outline-none" 
                  placeholder="Ask a question about mutual funds..." 
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
                <div className="absolute inset-y-0 right-md flex items-center gap-sm">
                  <button 
                    type="submit"
                    className="bg-primary text-on-primary px-lg py-sm rounded-lg font-label-md hover:opacity-90 active:scale-95 transition-all"
                  >
                    Search
                  </button>
                </div>
              </form>
            </div>

            {/* Answer Content */}
            <section className="max-w-3xl mx-auto space-y-lg">
              {/* Compliance Alert */}
              <div className="bg-surface-container-low border-l-4 border-tertiary p-md rounded-lg flex items-start gap-md">
                <span className="material-symbols-outlined text-tertiary" data-icon="warning">warning</span>
                <p className="text-body-sm text-on-surface-variant">
                  Information provided is based on the Scheme Information Document (SID). exit loads and metrics are subject to change by the AMC. Verify with the latest Key Information Memorandum (KIM) before investing.
                </p>
              </div>

              {/* Answer Card */}
              <article className="bg-surface-container-lowest faq-card-shadow rounded-xl p-xl">
                <div className="mb-lg">
                  <h2 className="font-headline-md text-headline-md text-on-surface mb-sm">{activeQuery}</h2>
                  <div className="h-1 w-16 bg-primary rounded-full"></div>
                </div>
                <div className="space-y-md text-body-md text-on-surface-variant leading-relaxed">
                  <p>{answerData.answer}</p>
                </div>

                {/* Citation Card */}
                <div className="mt-xl p-md rounded-lg citation-recess border border-outline-variant/30">
                  <div className="flex items-center gap-sm mb-xs">
                    <span className="material-symbols-outlined text-secondary text-sm" data-icon="menu_book">menu_book</span>
                    <span className="text-label-md font-bold text-on-surface">Primary Source</span>
                  </div>
                  <a 
                    className="text-primary text-body-sm hover:underline flex items-center gap-xs font-semibold" 
                    href={answerData.citation_url}
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    {getSourceDisplay(answerData.citation_url)}
                    <span className="material-symbols-outlined text-xs" data-icon="open_in_new">open_in_new</span>
                  </a>
                </div>

                {/* Card Footer */}
                <div className="mt-2xl pt-lg border-t border-outline-variant flex flex-col md:flex-row justify-between items-center gap-md">
                  <div className="flex items-center gap-sm">
                    <span className="material-symbols-outlined text-secondary text-body-sm" data-icon="verified" style={{ fontVariationSettings: "'FILL' 1" }}>verified</span>
                    <span className="text-body-sm text-outline">Last updated from sources: {answerData.last_updated}</span>
                  </div>
                  <div className="flex items-center gap-md">
                    <button 
                      onClick={handleCopy}
                      className="flex items-center gap-xs text-on-surface-variant hover:text-primary transition-colors text-label-md" 
                      title="Copy to clipboard"
                    >
                      <span className="material-symbols-outlined text-body-sm" data-icon={copied ? "done" : "content_copy"}>{copied ? "done" : "content_copy"}</span>
                      {copied ? 'Copied' : 'Copy'}
                    </button>
                    <div className="h-4 w-px bg-outline-variant"></div>
                    <button 
                      onClick={() => setVerifyOpen(true)}
                      className="flex items-center gap-xs text-on-surface-variant hover:text-primary transition-colors text-label-md" 
                      title="Verify source documentation"
                    >
                      <span className="material-symbols-outlined text-body-sm" data-icon="fact_check">fact_check</span>
                      Verify Source
                    </button>
                  </div>
                </div>
              </article>

              {/* Metadata Badges */}
              <div className="flex flex-wrap gap-sm">
                <span className="px-sm py-xs bg-secondary-container text-on-secondary-container rounded-full text-code-sm font-bold flex items-center gap-xs">
                  <span className="material-symbols-outlined text-xs" data-icon="check_circle" style={{ fontVariationSettings: "'FILL' 1" }}>check_circle</span>
                  Verified Facts Only
                </span>
                <span className="px-sm py-xs bg-surface-container-high text-on-surface-variant rounded-full text-code-sm font-bold">
                  Official Filings
                </span>
                <span className="px-sm py-xs bg-surface-container-high text-on-surface-variant rounded-full text-code-sm font-bold">
                  Regulatory Scoped
                </span>
              </div>
            </section>
          </div>
        )}

        {/* Refusal View */}
        {view === 'refusal' && (
          <div className="w-full max-w-max-width-desktop mx-auto px-margin-mobile md:px-lg py-3xl flex flex-col items-center">
            {/* Search Header */}
            <div className="w-full max-w-3xl mb-2xl">
              <form 
                onSubmit={(e) => { e.preventDefault(); handleSearch(); }}
                className="relative group"
              >
                <div className="absolute inset-y-0 left-0 pl-md flex items-center pointer-events-none">
                  <span className="material-symbols-outlined text-outline" data-icon="search">search</span>
                </div>
                <input 
                  className="block w-full pl-xl pr-32 py-lg bg-surface-container-lowest border-2 border-primary rounded-xl text-body-lg focus:outline-none shadow-sm transition-all"
                  placeholder="Ask a question..." 
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
                <div className="absolute inset-y-0 right-0 pr-sm flex items-center">
                  <button 
                    type="submit"
                    className="bg-primary text-on-primary px-lg py-sm rounded-lg font-label-md hover:opacity-90 transition-opacity"
                  >
                    Ask
                  </button>
                </div>
              </form>
              <p className="mt-sm text-body-sm text-on-surface-variant px-sm flex items-center gap-xs">
                <span className="material-symbols-outlined text-[16px]" data-icon="info">info</span>
                Intent check completed.
              </p>
            </div>

            {/* Refusal Bento Panel */}
            <div className="w-full max-w-4xl grid grid-cols-1 md:grid-cols-12 gap-lg">
              {/* Main Refusal message */}
              <section className="md:col-span-8 flex flex-col gap-lg">
                <div className="bg-surface-container-lowest border border-outline-variant rounded-xl p-xl shadow-sm relative overflow-hidden group">
                  {/* Left accent border */}
                  <div className="absolute left-0 top-0 bottom-0 w-1.5 bg-tertiary"></div>
                  <div className="flex items-start gap-md">
                    <div className="bg-tertiary-fixed text-on-tertiary-fixed p-md rounded-full">
                      <span className="material-symbols-outlined text-[32px]" data-icon="shield_lock" style={{ fontVariationSettings: "'FILL' 1" }}>shield_lock</span>
                    </div>
                    <div className="flex-grow">
                      <h2 className="font-headline-md text-headline-md text-on-surface mb-sm">Compliance Restriction</h2>
                      <p className="text-body-lg text-on-surface-variant leading-relaxed">
                        {answerData.answer}
                      </p>
                      <div className="mt-xl p-md bg-surface-container-low rounded-lg border border-outline-variant">
                        <p className="text-body-sm text-on-surface-variant italic">
                          "Under SEBI (Investment Advisers) Regulations, 2013, providing personalized investment suggestions or comparison-based advisories requires specific certifications which this automated information tool does not hold."
                        </p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Helpful paths */}
                <div className="bg-surface-container-highest rounded-xl p-lg border border-outline-variant">
                  <h3 className="font-label-md text-label-md uppercase tracking-wider text-outline mb-md">What I can help with instead:</h3>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-md">
                    <div 
                      onClick={() => handleSuggest('Who manages the HDFC Defence Fund?')}
                      className="flex items-center gap-sm p-sm bg-surface-container-lowest rounded-lg hover:border-primary border border-transparent cursor-pointer transition-all"
                    >
                      <span className="material-symbols-outlined text-primary" data-icon="groups">groups</span>
                      <span className="text-body-sm font-medium">Fund Manager Profile</span>
                    </div>
                    <div 
                      onClick={() => handleSuggest('What is the exit load of HDFC Small Cap Fund?')}
                      className="flex items-center gap-sm p-sm bg-surface-container-lowest rounded-lg hover:border-primary border border-transparent cursor-pointer transition-all"
                    >
                      <span className="material-symbols-outlined text-primary" data-icon="calculate">calculate</span>
                      <span className="text-body-sm font-medium">Expense Ratio &amp; Exit Load</span>
                    </div>
                    <div 
                      onClick={() => handleSuggest('What is the minimum SIP for HDFC Mid-Cap Fund?')}
                      className="flex items-center gap-sm p-sm bg-surface-container-lowest rounded-lg hover:border-primary border border-transparent cursor-pointer transition-all"
                    >
                      <span className="material-symbols-outlined text-primary" data-icon="description">description</span>
                      <span className="text-body-sm font-medium">Minimum Investment Details</span>
                    </div>
                    <div 
                      onClick={() => handleSuggest('What is the benchmark of HDFC Large Cap Fund?')}
                      className="flex items-center gap-sm p-sm bg-surface-container-lowest rounded-lg hover:border-primary border border-transparent cursor-pointer transition-all"
                    >
                      <span className="material-symbols-outlined text-primary" data-icon="analytics">analytics</span>
                      <span className="text-body-sm font-medium">Benchmark Indices</span>
                    </div>
                  </div>
                </div>
              </section>

              {/* Sidebar Resources */}
              <aside className="md:col-span-4 flex flex-col gap-lg">
                <div className="bg-surface-bright border border-outline-variant rounded-xl p-lg shadow-sm">
                  <h3 className="font-headline-md text-headline-md text-on-surface mb-lg flex items-center gap-sm">
                    <span className="material-symbols-outlined" data-icon="library_books">library_books</span>
                    Investor Hub
                  </h3>
                  <ul className="space-y-md">
                    <li>
                      <a 
                        className="group flex flex-col gap-xs p-sm rounded-lg hover:bg-surface-container-low transition-colors" 
                        href={answerData.citation_url}
                        target="_blank" 
                        rel="noopener noreferrer"
                      >
                        <div className="flex justify-between items-center">
                          <span className="text-body-md font-bold text-primary group-hover:underline">Official Resources</span>
                          <span className="material-symbols-outlined text-xs" data-icon="open_in_new">open_in_new</span>
                        </div>
                        <span className="text-body-sm text-on-surface-variant">SEBI &amp; AMFI investor education resources.</span>
                      </a>
                    </li>
                    <li>
                      <a 
                        className="group flex flex-col gap-xs p-sm rounded-lg hover:bg-surface-container-low transition-colors" 
                        href="https://www.sebi.gov.in"
                        target="_blank" 
                        rel="noopener noreferrer"
                      >
                        <div className="flex justify-between items-center">
                          <span className="text-body-md font-bold text-primary group-hover:underline">SEBI Portal</span>
                          <span className="material-symbols-outlined text-xs" data-icon="open_in_new">open_in_new</span>
                        </div>
                        <span className="text-body-sm text-on-surface-variant">Securities and Exchange Board of India homepage.</span>
                      </a>
                    </li>
                  </ul>
                </div>

                <div className="relative rounded-xl overflow-hidden h-40 bg-primary-container group">
                  <div className="absolute inset-0 bg-black/20 z-10"></div>
                  <img 
                    alt="Financial analysis desk" 
                    className="w-full h-full object-cover transform group-hover:scale-105 transition-transform duration-700" 
                    src="https://images.unsplash.com/photo-1454165804606-c3d57bc86b40?q=80&w=400&auto=format&fit=crop"
                  />
                  <div className="absolute bottom-md left-md z-20">
                    <span className="bg-secondary text-on-secondary px-sm py-xs rounded-full text-[10px] font-bold uppercase tracking-widest mb-xs inline-block">Notice</span>
                    <p className="text-on-primary-container font-bold text-body-sm">Consult a registered advisor for investment recommendations.</p>
                  </div>
                </div>
              </aside>
            </div>
          </div>
        )}
      </main>

      {/* Verify Popover Modal */}
      {verifyOpen && (
        <div className="fixed inset-0 bg-black/40 backdrop-blur-sm flex items-center justify-center z-[100] p-md">
          <div className="bg-surface rounded-xl shadow-2xl max-w-lg w-full p-xl border border-outline-variant">
            <div className="flex justify-between items-center mb-md">
              <h3 className="font-headline-md text-on-surface">Source Verification Chunks</h3>
              <button 
                className="text-outline hover:text-on-surface"
                onClick={() => setVerifyOpen(false)}
              >
                <span className="material-symbols-outlined" data-icon="close">close</span>
              </button>
            </div>
            
            <div className="bg-surface-container-highest p-md rounded-lg font-mono text-xs text-on-surface mb-md max-h-64 overflow-y-auto whitespace-pre-wrap leading-relaxed">
              {answerData.source_chunks && answerData.source_chunks.length > 0 ? (
                answerData.source_chunks.map((chunk, idx) => (
                  <div key={idx} className={`${idx > 0 ? 'mt-4 pt-4 border-t border-outline-variant/30' : ''}`}>
                    <div className="font-semibold text-primary mb-1">[Chunk {idx + 1}]</div>
                    {chunk}
                  </div>
                ))
              ) : (
                "Verified facts loaded from: " + answerData.citation_url
              )}
            </div>

            <div className="flex justify-end">
              <button 
                className="bg-primary text-on-primary px-lg py-sm rounded-lg font-label-md hover:opacity-90 active:scale-95" 
                onClick={() => setVerifyOpen(false)}
              >
                Close Window
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-surface-container-low border-t border-outline-variant mt-auto">
        <div className="flex flex-col md:flex-row justify-between items-center px-lg py-xl w-full max-w-max-width-desktop mx-auto gap-md">
          <div className="flex flex-col gap-xs items-center md:items-start">
            <span className="font-label-md text-label-md font-bold text-on-surface">Mutual Fund FAQ Assistant</span>
            <p className="font-body-sm text-body-sm text-on-surface-variant">
              © {new Date().getFullYear()} Mutual Fund FAQ Assistant. All rights reserved. Sourced from official scheme information documents.
            </p>
          </div>
          <nav className="flex flex-wrap justify-center gap-lg">
            <a className="text-on-surface-variant hover:text-primary transition-colors text-body-sm" href="https://www.amfiindia.com" target="_blank" rel="noreferrer">AMFI Regulatory</a>
            <a className="text-on-surface-variant hover:text-primary transition-colors text-body-sm" href="https://www.sebi.gov.in" target="_blank" rel="noreferrer">SEBI Investor Charter</a>
          </nav>
        </div>
      </footer>
    </>
  );
}

export default App;
