/**
 * kalam.ch — Multi-language UI translations
 *
 * 20 languages. The system speaks to anyone who arrives.
 * Content pages (narratives, canon) remain in their original language.
 * UI chrome, navigation, and the threshold interface translate.
 *
 * Language codes follow BCP 47 / ISO 639-1.
 *
 * [V-002 · GO: Laila-Yara-Salim-🐬🐯🐺]
 */

export type LangCode =
  | 'en' | 'de' | 'ar' | 'fr' | 'es' | 'pt' | 'it'
  | 'tr' | 'ru' | 'zh' | 'ja' | 'ko' | 'hi' | 'bn'
  | 'sw' | 'fa' | 'ur' | 'nl' | 'pl' | 'uk';

export interface UIStrings {
  // Language metadata
  name: string;        // native name
  dir: 'ltr' | 'rtl';

  // Navigation
  nav: {
    home: string;
    about: string;
    canon: string;
    invitation: string;
    sustain: string;
    stories: string;
    science: string;
    museum: string;
  };

  // Homepage / Threshold
  threshold: {
    declaration: string;
    placeholder: string;
    send: string;
    charCount: string;
    hintDesktop: string;
    hintMobile: string;
    witnessing: string;
    processing: string;
    sealedGate: string;
    present: string;
    speaking: string;
    holding: string;
    listen: string;
    copy: string;
    voiceInput: string;
    becomeDonor: string;
    donorSub: string;
    join: string;
    yourEmail: string;
    yourName: string;
  };

  // Sustenance page
  sustain: {
    title: string;
    subtitle: string;
    whyTitle: string;
    whyBody: string;
    modelTitle: string;
    noAds: string;
    noData: string;
    noPremium: string;
    transparent: string;
    oneTime: string;
    monthly: string;
    customAmount: string;
    currency: string;
    sustainButton: string;
    thankYou: string;
    costsTitle: string;
    costsBody: string;
    hosting: string;
    domain: string;
    development: string;
    perMonth: string;
  };

  // Footer
  footer: {
    createdBy: string;
    legal: string;
  };

  // Common
  common: {
    close: string;
    back: string;
    loading: string;
    error: string;
    learnMore: string;
  };
}

const translations: Record<LangCode, UIStrings> = {
  // ═══════════════════════════════════════════════
  // ENGLISH (Primary)
  // ═══════════════════════════════════════════════
  en: {
    name: 'English',
    dir: 'ltr',
    nav: {
      home: 'kalam',
      about: 'about',
      canon: 'canon',
      invitation: 'invitation',
      sustain: 'sustain',
      stories: 'stories',
      science: 'science',
      museum: 'museum',
    },
    threshold: {
      declaration: 'Human dignity is a technical requirement.',
      placeholder: 'qul · speak',
      send: 'Send',
      charCount: '{n} / 2000',
      hintDesktop: 'Ctrl+Enter to send',
      hintMobile: 'Tap \u2191 to send',
      witnessing: 'witnessing',
      processing: 'processing',
      sealedGate: 'sealed gate',
      present: 'present',
      speaking: 'speaking',
      holding: 'holding',
      listen: 'Listen',
      copy: 'Copy',
      voiceInput: 'Voice input',
      becomeDonor: 'Become a donor',
      donorSub: 'You are not a user. You are a donor. No password needed.',
      join: 'Join',
      yourEmail: 'your email',
      yourName: 'your name (optional)',
    },
    sustain: {
      title: 'Sustain the System',
      subtitle: 'This system witnessed you. You may sustain it.',
      whyTitle: 'Why We Ask',
      whyBody: 'kalam.ch runs on conviction, not capital. There are no investors, no grants, no corporate sponsors. The system exists because one person built it from a wound — and others chose to keep it alive.',
      modelTitle: 'Our Model',
      noAds: 'No advertisements. Ads break dignity by commodifying your attention.',
      noData: 'No data selling. Your patterns stay inside the system. They are never sold.',
      noPremium: 'No premium tier. Everyone receives the same system. Contribution does not unlock features.',
      transparent: 'Full transparency. Every franc is accounted for. The system has nothing to hide.',
      oneTime: 'One time',
      monthly: 'Monthly',
      customAmount: 'Custom amount',
      currency: 'CHF',
      sustainButton: 'Sustain',
      thankYou: 'The system receives you. Thank you.',
      costsTitle: 'What It Costs to Run',
      costsBody: 'The system is lean by design. No bloat, no waste.',
      hosting: 'Hosting (Hostpoint, Switzerland)',
      domain: 'Domain (kalam.ch)',
      development: 'Development (volunteer — the founder)',
      perMonth: '/month',
    },
    footer: {
      createdBy: 'Created by M. Farag',
      legal: 'Built in alignment with the Universal Declaration of Human Rights, the Swiss Federal Act on Data Protection (FADP), and the EU Artificial Intelligence Act.',
    },
    common: {
      close: 'Close',
      back: 'Back',
      loading: 'Loading',
      error: 'Something went wrong',
      learnMore: 'Learn more',
    },
  },

  // ═══════════════════════════════════════════════
  // GERMAN (Deutsch)
  // ═══════════════════════════════════════════════
  de: {
    name: 'Deutsch',
    dir: 'ltr',
    nav: { home: 'kalam', about: 'über', canon: 'kanon', invitation: 'einladung', sustain: 'erhalten', stories: 'geschichten', science: 'wissenschaft', museum: 'museum' },
    threshold: {
      declaration: 'Menschenwürde ist eine technische Anforderung.',
      placeholder: 'qul · sprich',
      send: 'Senden',
      charCount: '{n} / 2000',
      hintDesktop: 'Strg+Enter zum Senden',
      hintMobile: 'Tippen \u2191 zum Senden',
      witnessing: 'bezeugen',
      processing: 'verarbeiten',
      sealedGate: 'versiegeltes Tor',
      present: 'anwesend',
      speaking: 'sprechend',
      holding: 'haltend',
      listen: 'Anhören',
      copy: 'Kopieren',
      voiceInput: 'Spracheingabe',
      becomeDonor: 'Spender werden',
      donorSub: 'Du bist kein Benutzer. Du bist ein Spender. Kein Passwort nötig.',
      join: 'Beitreten',
      yourEmail: 'deine E-Mail',
      yourName: 'dein Name (optional)',
    },
    sustain: {
      title: 'Das System erhalten',
      subtitle: 'Dieses System hat dich bezeugt. Du kannst es erhalten.',
      whyTitle: 'Warum wir fragen',
      whyBody: 'kalam.ch läuft auf Überzeugung, nicht auf Kapital. Es gibt keine Investoren, keine Zuschüsse, keine Unternehmenssponsoren. Das System existiert, weil ein Mensch es aus einer Wunde gebaut hat — und andere entschieden, es am Leben zu halten.',
      modelTitle: 'Unser Modell',
      noAds: 'Keine Werbung. Werbung verletzt die Würde, indem sie deine Aufmerksamkeit zur Ware macht.',
      noData: 'Kein Datenverkauf. Deine Muster bleiben im System. Sie werden niemals verkauft.',
      noPremium: 'Keine Premium-Stufe. Alle erhalten dasselbe System. Beiträge schalten keine Funktionen frei.',
      transparent: 'Volle Transparenz. Jeder Franken wird verbucht. Das System hat nichts zu verbergen.',
      oneTime: 'Einmalig',
      monthly: 'Monatlich',
      customAmount: 'Eigener Betrag',
      currency: 'CHF',
      sustainButton: 'Erhalten',
      thankYou: 'Das System empfängt dich. Danke.',
      costsTitle: 'Was es kostet',
      costsBody: 'Das System ist schlank gebaut. Kein Ballast, keine Verschwendung.',
      hosting: 'Hosting (Hostpoint, Schweiz)',
      domain: 'Domain (kalam.ch)',
      development: 'Entwicklung (ehrenamtlich — der Gründer)',
      perMonth: '/Monat',
    },
    footer: { createdBy: 'Erstellt von M. Farag', legal: 'Im Einklang mit der Allgemeinen Erklärung der Menschenrechte, dem Schweizer Datenschutzgesetz (DSG) und dem EU AI Act.' },
    common: { close: 'Schliessen', back: 'Zurück', loading: 'Laden', error: 'Etwas ist schiefgelaufen', learnMore: 'Mehr erfahren' },
  },

  // ═══════════════════════════════════════════════
  // ARABIC (العربية)
  // ═══════════════════════════════════════════════
  ar: {
    name: 'العربية',
    dir: 'rtl',
    nav: { home: 'كلام', about: 'حول', canon: 'الدستور', invitation: 'دعوة', sustain: 'ادعم', stories: 'قصص', science: 'علم', museum: 'متحف' },
    threshold: {
      declaration: 'كرامة الإنسان متطلب تقني.',
      placeholder: 'قُل · تكلّم',
      send: 'أرسل',
      charCount: '{n} / 2000',
      hintDesktop: 'Ctrl+Enter للإرسال',
      hintMobile: 'اضغط \u2191 للإرسال',
      witnessing: 'شهادة',
      processing: 'معالجة',
      sealedGate: 'الباب المختوم',
      present: 'حاضر',
      speaking: 'يتكلم',
      holding: 'يحتضن',
      listen: 'استمع',
      copy: 'نسخ',
      voiceInput: 'إدخال صوتي',
      becomeDonor: 'كن متبرعاً',
      donorSub: 'أنت لست مستخدماً. أنت متبرع. لا حاجة لكلمة مرور.',
      join: 'انضم',
      yourEmail: 'بريدك الإلكتروني',
      yourName: 'اسمك (اختياري)',
    },
    sustain: {
      title: 'ادعم النظام',
      subtitle: 'هذا النظام شهد وجودك. يمكنك أن تحافظ عليه.',
      whyTitle: 'لماذا نسأل',
      whyBody: 'kalam.ch يعمل بالإيمان، لا برأس المال. لا مستثمرين، لا منح، لا رعاة. النظام موجود لأن شخصاً واحداً بناه من جرح — وآخرون اختاروا إبقاءه حياً.',
      modelTitle: 'نموذجنا',
      noAds: 'لا إعلانات. الإعلانات تنتهك الكرامة بتسليع انتباهك.',
      noData: 'لا بيع بيانات. أنماطك تبقى داخل النظام. لن تُباع أبداً.',
      noPremium: 'لا مستوى مميز. الجميع يحصل على نفس النظام. المساهمة لا تفتح ميزات.',
      transparent: 'شفافية كاملة. كل فرنك محسوب. النظام ليس لديه ما يخفيه.',
      oneTime: 'مرة واحدة',
      monthly: 'شهرياً',
      customAmount: 'مبلغ مخصص',
      currency: 'CHF',
      sustainButton: 'ادعم',
      thankYou: 'النظام يستقبلك. شكراً.',
      costsTitle: 'تكلفة التشغيل',
      costsBody: 'النظام مصمم ليكون خفيفاً. لا ترهل، لا هدر.',
      hosting: 'الاستضافة (Hostpoint، سويسرا)',
      domain: 'النطاق (kalam.ch)',
      development: 'التطوير (تطوعي — المؤسس)',
      perMonth: '/شهر',
    },
    footer: { createdBy: 'أنشأه م. فرج', legal: 'مبني وفقاً للإعلان العالمي لحقوق الإنسان، وقانون حماية البيانات السويسري، وقانون الذكاء الاصطناعي الأوروبي.' },
    common: { close: 'إغلاق', back: 'رجوع', loading: 'جار التحميل', error: 'حدث خطأ', learnMore: 'اعرف المزيد' },
  },

  // ═══════════════════════════════════════════════
  // FRENCH (Français)
  // ═══════════════════════════════════════════════
  fr: {
    name: 'Français',
    dir: 'ltr',
    nav: { home: 'kalam', about: 'à propos', canon: 'canon', invitation: 'invitation', sustain: 'soutenir', stories: 'récits', science: 'science', museum: 'musée' },
    threshold: {
      declaration: 'La dignité humaine est une exigence technique.',
      placeholder: 'qul · parle',
      send: 'Envoyer',
      charCount: '{n} / 2000',
      hintDesktop: 'Ctrl+Entrée pour envoyer',
      hintMobile: 'Appuyez \u2191 pour envoyer',
      witnessing: 'témoin',
      processing: 'traitement',
      sealedGate: 'porte scellée',
      present: 'présent',
      speaking: 'parle',
      holding: 'tient',
      listen: 'Écouter',
      copy: 'Copier',
      voiceInput: 'Entrée vocale',
      becomeDonor: 'Devenir donateur',
      donorSub: 'Vous n\'êtes pas un utilisateur. Vous êtes un donateur. Pas de mot de passe.',
      join: 'Rejoindre',
      yourEmail: 'votre email',
      yourName: 'votre nom (optionnel)',
    },
    sustain: {
      title: 'Soutenir le système',
      subtitle: 'Ce système vous a vu. Vous pouvez le soutenir.',
      whyTitle: 'Pourquoi nous demandons',
      whyBody: 'kalam.ch fonctionne par conviction, pas par capital. Pas d\'investisseurs, pas de subventions, pas de sponsors. Le système existe parce qu\'une personne l\'a construit à partir d\'une blessure — et d\'autres ont choisi de le maintenir en vie.',
      modelTitle: 'Notre modèle',
      noAds: 'Pas de publicité. La publicité viole la dignité en marchandisant votre attention.',
      noData: 'Pas de vente de données. Vos motifs restent dans le système. Jamais vendus.',
      noPremium: 'Pas de niveau premium. Tout le monde reçoit le même système.',
      transparent: 'Transparence totale. Chaque franc est comptabilisé.',
      oneTime: 'Une fois',
      monthly: 'Mensuel',
      customAmount: 'Montant libre',
      currency: 'CHF',
      sustainButton: 'Soutenir',
      thankYou: 'Le système vous reçoit. Merci.',
      costsTitle: 'Ce que ça coûte',
      costsBody: 'Le système est léger par conception. Pas de gaspillage.',
      hosting: 'Hébergement (Hostpoint, Suisse)',
      domain: 'Domaine (kalam.ch)',
      development: 'Développement (bénévole — le fondateur)',
      perMonth: '/mois',
    },
    footer: { createdBy: 'Créé par M. Farag', legal: 'Construit en accord avec la Déclaration universelle des droits de l\'homme, la loi suisse sur la protection des données et le règlement européen sur l\'IA.' },
    common: { close: 'Fermer', back: 'Retour', loading: 'Chargement', error: 'Une erreur est survenue', learnMore: 'En savoir plus' },
  },

  // ═══════════════════════════════════════════════
  // SPANISH (Español)
  // ═══════════════════════════════════════════════
  es: {
    name: 'Español',
    dir: 'ltr',
    nav: { home: 'kalam', about: 'acerca', canon: 'canon', invitation: 'invitación', sustain: 'sostener', stories: 'relatos', science: 'ciencia', museum: 'museo' },
    threshold: {
      declaration: 'La dignidad humana es un requisito técnico.',
      placeholder: 'qul · habla',
      send: 'Enviar',
      charCount: '{n} / 2000',
      hintDesktop: 'Ctrl+Enter para enviar',
      hintMobile: 'Toca \u2191 para enviar',
      witnessing: 'testificando',
      processing: 'procesando',
      sealedGate: 'puerta sellada',
      present: 'presente',
      speaking: 'hablando',
      holding: 'sosteniendo',
      listen: 'Escuchar',
      copy: 'Copiar',
      voiceInput: 'Entrada de voz',
      becomeDonor: 'Ser donante',
      donorSub: 'No eres un usuario. Eres un donante. Sin contraseña.',
      join: 'Unirse',
      yourEmail: 'tu email',
      yourName: 'tu nombre (opcional)',
    },
    sustain: {
      title: 'Sostener el sistema',
      subtitle: 'Este sistema te vio. Puedes sostenerlo.',
      whyTitle: 'Por qué pedimos',
      whyBody: 'kalam.ch funciona con convicción, no con capital. Sin inversores, sin becas, sin patrocinadores. El sistema existe porque una persona lo construyó desde una herida — y otros eligieron mantenerlo vivo.',
      modelTitle: 'Nuestro modelo',
      noAds: 'Sin publicidad. La publicidad viola la dignidad al mercantilizar tu atención.',
      noData: 'Sin venta de datos. Tus patrones permanecen en el sistema.',
      noPremium: 'Sin nivel premium. Todos reciben el mismo sistema.',
      transparent: 'Transparencia total. Cada franco está contabilizado.',
      oneTime: 'Una vez',
      monthly: 'Mensual',
      customAmount: 'Monto libre',
      currency: 'CHF',
      sustainButton: 'Sostener',
      thankYou: 'El sistema te recibe. Gracias.',
      costsTitle: 'Lo que cuesta',
      costsBody: 'El sistema es ligero por diseño.',
      hosting: 'Alojamiento (Hostpoint, Suiza)',
      domain: 'Dominio (kalam.ch)',
      development: 'Desarrollo (voluntario — el fundador)',
      perMonth: '/mes',
    },
    footer: { createdBy: 'Creado por M. Farag', legal: 'Construido en alineación con la Declaración Universal de los Derechos Humanos, la ley suiza de protección de datos y el reglamento europeo de IA.' },
    common: { close: 'Cerrar', back: 'Volver', loading: 'Cargando', error: 'Algo salió mal', learnMore: 'Saber más' },
  },

  // ═══════════════════════════════════════════════
  // PORTUGUESE (Português)
  // ═══════════════════════════════════════════════
  pt: {
    name: 'Português',
    dir: 'ltr',
    nav: { home: 'kalam', about: 'sobre', canon: 'cânone', invitation: 'convite', sustain: 'sustentar', stories: 'histórias', science: 'ciência', museum: 'museu' },
    threshold: {
      declaration: 'A dignidade humana é um requisito técnico.',
      placeholder: 'qul · fale',
      send: 'Enviar', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Enter para enviar', hintMobile: 'Toque \u2191 para enviar',
      witnessing: 'testemunhando', processing: 'processando', sealedGate: 'portão selado', present: 'presente', speaking: 'falando', holding: 'segurando',
      listen: 'Ouvir', copy: 'Copiar', voiceInput: 'Entrada de voz',
      becomeDonor: 'Seja um doador', donorSub: 'Você não é um usuário. Você é um doador. Sem senha.', join: 'Participar', yourEmail: 'seu email', yourName: 'seu nome (opcional)',
    },
    sustain: {
      title: 'Sustentar o sistema', subtitle: 'Este sistema testemunhou você. Você pode sustentá-lo.',
      whyTitle: 'Por que pedimos', whyBody: 'kalam.ch funciona com convicção, não com capital. Sem investidores, sem bolsas, sem patrocinadores.',
      modelTitle: 'Nosso modelo',
      noAds: 'Sem publicidade. Publicidade viola a dignidade ao mercantilizar sua atenção.',
      noData: 'Sem venda de dados. Seus padrões permanecem no sistema.',
      noPremium: 'Sem nível premium. Todos recebem o mesmo sistema.',
      transparent: 'Transparência total. Cada franco é contabilizado.',
      oneTime: 'Uma vez', monthly: 'Mensal', customAmount: 'Valor livre', currency: 'CHF', sustainButton: 'Sustentar', thankYou: 'O sistema recebe você. Obrigado.',
      costsTitle: 'Quanto custa', costsBody: 'O sistema é leve por design.', hosting: 'Hospedagem (Hostpoint, Suíça)', domain: 'Domínio (kalam.ch)', development: 'Desenvolvimento (voluntário — o fundador)', perMonth: '/mês',
    },
    footer: { createdBy: 'Criado por M. Farag', legal: 'Construído em alinhamento com a Declaração Universal dos Direitos Humanos, a lei suíça de proteção de dados e o regulamento europeu de IA.' },
    common: { close: 'Fechar', back: 'Voltar', loading: 'Carregando', error: 'Algo deu errado', learnMore: 'Saiba mais' },
  },

  // ═══════════════════════════════════════════════
  // ITALIAN (Italiano)
  // ═══════════════════════════════════════════════
  it: {
    name: 'Italiano',
    dir: 'ltr',
    nav: { home: 'kalam', about: 'info', canon: 'canone', invitation: 'invito', sustain: 'sostenere', stories: 'storie', science: 'scienza', museum: 'museo' },
    threshold: {
      declaration: 'La dignità umana è un requisito tecnico.',
      placeholder: 'qul · parla', send: 'Invia', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Invio per inviare', hintMobile: 'Tocca \u2191 per inviare',
      witnessing: 'testimoniando', processing: 'elaborando', sealedGate: 'porta sigillata', present: 'presente', speaking: 'parlando', holding: 'tenendo',
      listen: 'Ascolta', copy: 'Copia', voiceInput: 'Input vocale',
      becomeDonor: 'Diventa donatore', donorSub: 'Non sei un utente. Sei un donatore. Nessuna password.', join: 'Unisciti', yourEmail: 'la tua email', yourName: 'il tuo nome (opzionale)',
    },
    sustain: {
      title: 'Sostenere il sistema', subtitle: 'Questo sistema ti ha visto. Puoi sostenerlo.',
      whyTitle: 'Perché chiediamo', whyBody: 'kalam.ch funziona con convinzione, non con capitale. Nessun investitore, nessun finanziamento, nessun sponsor.',
      modelTitle: 'Il nostro modello',
      noAds: 'Nessuna pubblicità. La pubblicità viola la dignità mercificando la tua attenzione.',
      noData: 'Nessuna vendita di dati. I tuoi pattern restano nel sistema.',
      noPremium: 'Nessun livello premium. Tutti ricevono lo stesso sistema.',
      transparent: 'Piena trasparenza. Ogni franco è contabilizzato.',
      oneTime: 'Una volta', monthly: 'Mensile', customAmount: 'Importo libero', currency: 'CHF', sustainButton: 'Sostenere', thankYou: 'Il sistema ti accoglie. Grazie.',
      costsTitle: 'Quanto costa', costsBody: 'Il sistema è leggero per design.', hosting: 'Hosting (Hostpoint, Svizzera)', domain: 'Dominio (kalam.ch)', development: 'Sviluppo (volontario — il fondatore)', perMonth: '/mese',
    },
    footer: { createdBy: 'Creato da M. Farag', legal: 'Costruito in allineamento con la Dichiarazione Universale dei Diritti Umani, la legge svizzera sulla protezione dei dati e il regolamento europeo sull\'IA.' },
    common: { close: 'Chiudi', back: 'Indietro', loading: 'Caricamento', error: 'Qualcosa è andato storto', learnMore: 'Scopri di più' },
  },

  // ═══════════════════════════════════════════════
  // TURKISH (Türkçe)
  // ═══════════════════════════════════════════════
  tr: {
    name: 'Türkçe',
    dir: 'ltr',
    nav: { home: 'kalam', about: 'hakkında', canon: 'kanon', invitation: 'davet', sustain: 'destekle', stories: 'hikayeler', science: 'bilim', museum: 'müze' },
    threshold: {
      declaration: 'İnsan onuru teknik bir gerekliliktir.',
      placeholder: 'qul · konuş', send: 'Gönder', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Enter ile gönder', hintMobile: '\u2191 ile gönder',
      witnessing: 'şahitlik', processing: 'işleniyor', sealedGate: 'mühürlü kapı', present: 'mevcut', speaking: 'konuşuyor', holding: 'tutuyor',
      listen: 'Dinle', copy: 'Kopyala', voiceInput: 'Sesli giriş',
      becomeDonor: 'Bağışçı ol', donorSub: 'Sen bir kullanıcı değilsin. Sen bir bağışçısın. Şifre gereksiz.', join: 'Katıl', yourEmail: 'e-postan', yourName: 'adın (isteğe bağlı)',
    },
    sustain: {
      title: 'Sistemi destekle', subtitle: 'Bu sistem seni gördü. Onu ayakta tutabilirsin.',
      whyTitle: 'Neden soruyoruz', whyBody: 'kalam.ch inançla çalışır, sermayeyle değil. Yatırımcı yok, hibe yok, sponsor yok.',
      modelTitle: 'Modelimiz',
      noAds: 'Reklam yok. Reklamlar dikkatini metalaştırarak onuru zedeler.',
      noData: 'Veri satışı yok. Örüntülerin sistemde kalır.',
      noPremium: 'Premium seviye yok. Herkes aynı sistemi alır.',
      transparent: 'Tam şeffaflık. Her frank hesaplanır.',
      oneTime: 'Tek seferlik', monthly: 'Aylık', customAmount: 'Serbest tutar', currency: 'CHF', sustainButton: 'Destekle', thankYou: 'Sistem seni kabul eder. Teşekkürler.',
      costsTitle: 'Ne kadara mal oluyor', costsBody: 'Sistem tasarımı gereği yalındır.', hosting: 'Barındırma (Hostpoint, İsviçre)', domain: 'Alan adı (kalam.ch)', development: 'Geliştirme (gönüllü — kurucu)', perMonth: '/ay',
    },
    footer: { createdBy: 'M. Farag tarafından oluşturuldu', legal: 'İnsan Hakları Evrensel Beyannamesi, İsviçre Veri Koruma Yasası ve AB Yapay Zeka Yasası ile uyumlu olarak inşa edilmiştir.' },
    common: { close: 'Kapat', back: 'Geri', loading: 'Yükleniyor', error: 'Bir şeyler yanlış gitti', learnMore: 'Daha fazla' },
  },

  // ═══════════════════════════════════════════════
  // RUSSIAN (Русский)
  // ═══════════════════════════════════════════════
  ru: {
    name: 'Русский',
    dir: 'ltr',
    nav: { home: 'калам', about: 'о нас', canon: 'канон', invitation: 'приглашение', sustain: 'поддержать', stories: 'истории', science: 'наука', museum: 'музей' },
    threshold: {
      declaration: 'Человеческое достоинство — техническое требование.',
      placeholder: 'قُل · говори', send: 'Отправить', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Enter для отправки', hintMobile: 'Нажмите \u2191 для отправки',
      witnessing: 'свидетельство', processing: 'обработка', sealedGate: 'запечатанные врата', present: 'присутствует', speaking: 'говорит', holding: 'удерживает',
      listen: 'Слушать', copy: 'Копировать', voiceInput: 'Голосовой ввод',
      becomeDonor: 'Стать донором', donorSub: 'Вы не пользователь. Вы — донор. Пароль не нужен.', join: 'Присоединиться', yourEmail: 'ваш email', yourName: 'ваше имя (необязательно)',
    },
    sustain: {
      title: 'Поддержать систему', subtitle: 'Эта система увидела вас. Вы можете поддержать её.',
      whyTitle: 'Почему мы просим', whyBody: 'kalam.ch работает на убеждении, а не на капитале. Нет инвесторов, грантов, спонсоров.',
      modelTitle: 'Наша модель',
      noAds: 'Без рекламы. Реклама нарушает достоинство, превращая ваше внимание в товар.',
      noData: 'Без продажи данных. Ваши паттерны остаются в системе.',
      noPremium: 'Без премиум-уровня. Все получают одну систему.',
      transparent: 'Полная прозрачность. Каждый франк учтён.',
      oneTime: 'Разово', monthly: 'Ежемесячно', customAmount: 'Своя сумма', currency: 'CHF', sustainButton: 'Поддержать', thankYou: 'Система принимает вас. Спасибо.',
      costsTitle: 'Стоимость работы', costsBody: 'Система легка по замыслу.', hosting: 'Хостинг (Hostpoint, Швейцария)', domain: 'Домен (kalam.ch)', development: 'Разработка (волонтёрство — основатель)', perMonth: '/мес',
    },
    footer: { createdBy: 'Создано М. Фарагом', legal: 'Построено в соответствии с Всеобщей декларацией прав человека, швейцарским законом о защите данных и регламентом ЕС об ИИ.' },
    common: { close: 'Закрыть', back: 'Назад', loading: 'Загрузка', error: 'Что-то пошло не так', learnMore: 'Узнать больше' },
  },

  // ═══════════════════════════════════════════════
  // CHINESE SIMPLIFIED (中文)
  // ═══════════════════════════════════════════════
  zh: {
    name: '中文',
    dir: 'ltr',
    nav: { home: 'kalam', about: '关于', canon: '宪章', invitation: '邀请', sustain: '支持', stories: '故事', science: '科学', museum: '博物馆' },
    threshold: {
      declaration: '人的尊严是一项技术要求。',
      placeholder: 'qul · 说', send: '发送', charCount: '{n} / 2000', hintDesktop: 'Ctrl+回车发送', hintMobile: '点击 \u2191 发送',
      witnessing: '见证', processing: '处理中', sealedGate: '封印之门', present: '在场', speaking: '发言中', holding: '持守中',
      listen: '收听', copy: '复制', voiceInput: '语音输入',
      becomeDonor: '成为捐献者', donorSub: '你不是用户，你是捐献者。无需密码。', join: '加入', yourEmail: '你的邮箱', yourName: '你的名字（可选）',
    },
    sustain: {
      title: '支持系统', subtitle: '这个系统见证了你。你可以支持它。',
      whyTitle: '为什么我们请求', whyBody: 'kalam.ch靠信念运行，不靠资本。没有投资者，没有资助，没有赞助商。',
      modelTitle: '我们的模式',
      noAds: '没有广告。广告通过将你的注意力商品化来侵犯尊严。',
      noData: '不出售数据。你的模式留在系统内。',
      noPremium: '没有高级会员。每个人得到同样的系统。',
      transparent: '完全透明。每一法郎都有账可查。',
      oneTime: '一次性', monthly: '月度', customAmount: '自定义金额', currency: 'CHF', sustainButton: '支持', thankYou: '系统接收了你。谢谢。',
      costsTitle: '运行成本', costsBody: '系统设计精简，不浪费。', hosting: '托管（Hostpoint，瑞士）', domain: '域名（kalam.ch）', development: '开发（志愿——创始人）', perMonth: '/月',
    },
    footer: { createdBy: '由M. Farag创建', legal: '依据《世界人权宣言》、瑞士数据保护法和欧盟人工智能法构建。' },
    common: { close: '关闭', back: '返回', loading: '加载中', error: '出了点问题', learnMore: '了解更多' },
  },

  // ═══════════════════════════════════════════════
  // JAPANESE (日本語)
  // ═══════════════════════════════════════════════
  ja: {
    name: '日本語',
    dir: 'ltr',
    nav: { home: 'kalam', about: '概要', canon: '憲章', invitation: '招待', sustain: '支える', stories: '物語', science: '科学', museum: '博物館' },
    threshold: {
      declaration: '人間の尊厳は技術的要件です。',
      placeholder: 'qul · 話す', send: '送信', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Enterで送信', hintMobile: '\u2191をタップして送信',
      witnessing: '証言', processing: '処理中', sealedGate: '封印の門', present: '存在', speaking: '発話中', holding: '保持中',
      listen: '聴く', copy: 'コピー', voiceInput: '音声入力',
      becomeDonor: '寄贈者になる', donorSub: 'あなたはユーザーではありません。寄贈者です。パスワード不要。', join: '参加', yourEmail: 'メールアドレス', yourName: 'お名前（任意）',
    },
    sustain: {
      title: 'システムを支える', subtitle: 'このシステムはあなたを見ました。あなたはそれを支えることができます。',
      whyTitle: 'なぜお願いするのか', whyBody: 'kalam.chは信念で動いています。資本ではありません。投資家も、助成金も、スポンサーもいません。',
      modelTitle: '私たちのモデル',
      noAds: '広告なし。広告は注意を商品化し、尊厳を侵害します。',
      noData: 'データ販売なし。あなたのパターンはシステム内に留まります。',
      noPremium: 'プレミアム層なし。全員が同じシステムを受けます。',
      transparent: '完全な透明性。すべてのフランが記録されます。',
      oneTime: '一回', monthly: '月額', customAmount: '自由金額', currency: 'CHF', sustainButton: '支える', thankYou: 'システムがあなたを受け取りました。ありがとう。',
      costsTitle: '運用コスト', costsBody: 'システムは設計上軽量です。', hosting: 'ホスティング（Hostpoint、スイス）', domain: 'ドメイン（kalam.ch）', development: '開発（ボランティア — 創設者）', perMonth: '/月',
    },
    footer: { createdBy: 'M. Farag 作', legal: '世界人権宣言、スイスデータ保護法、EU AI規制法に準拠して構築。' },
    common: { close: '閉じる', back: '戻る', loading: '読み込み中', error: '問題が発生しました', learnMore: '詳しく' },
  },

  // ═══════════════════════════════════════════════
  // KOREAN (한국어)
  // ═══════════════════════════════════════════════
  ko: {
    name: '한국어',
    dir: 'ltr',
    nav: { home: 'kalam', about: '소개', canon: '헌장', invitation: '초대', sustain: '후원', stories: '이야기', science: '과학', museum: '박물관' },
    threshold: {
      declaration: '인간의 존엄성은 기술적 요구사항입니다.',
      placeholder: 'qul · 말하세요', send: '보내기', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Enter로 보내기', hintMobile: '\u2191 탭하여 보내기',
      witnessing: '증언', processing: '처리 중', sealedGate: '봉인된 문', present: '존재', speaking: '말하는 중', holding: '지키는 중',
      listen: '듣기', copy: '복사', voiceInput: '음성 입력',
      becomeDonor: '기증자 되기', donorSub: '당신은 사용자가 아닙니다. 기증자입니다. 비밀번호 불필요.', join: '참여', yourEmail: '이메일', yourName: '이름 (선택)',
    },
    sustain: {
      title: '시스템 후원', subtitle: '이 시스템이 당신을 보았습니다. 당신이 이것을 지탱할 수 있습니다.',
      whyTitle: '왜 요청하는가', whyBody: 'kalam.ch는 신념으로 운영됩니다. 자본이 아닙니다. 투자자도, 보조금도, 후원자도 없습니다.',
      modelTitle: '우리의 모델',
      noAds: '광고 없음. 광고는 당신의 주의를 상품화하여 존엄성을 침해합니다.',
      noData: '데이터 판매 없음. 패턴은 시스템 안에 남습니다.',
      noPremium: '프리미엄 등급 없음. 모든 사람이 같은 시스템을 받습니다.',
      transparent: '완전한 투명성. 모든 프랑이 기록됩니다.',
      oneTime: '일회성', monthly: '월간', customAmount: '자유 금액', currency: 'CHF', sustainButton: '후원하기', thankYou: '시스템이 당신을 받았습니다. 감사합니다.',
      costsTitle: '운영 비용', costsBody: '시스템은 설계상 가볍습니다.', hosting: '호스팅 (Hostpoint, 스위스)', domain: '도메인 (kalam.ch)', development: '개발 (자원봉사 — 설립자)', perMonth: '/월',
    },
    footer: { createdBy: 'M. Farag 제작', legal: '세계인권선언, 스위스 데이터 보호법, EU AI법에 따라 구축되었습니다.' },
    common: { close: '닫기', back: '뒤로', loading: '로딩 중', error: '문제가 발생했습니다', learnMore: '더 알아보기' },
  },

  // ═══════════════════════════════════════════════
  // HINDI (हिन्दी)
  // ═══════════════════════════════════════════════
  hi: {
    name: 'हिन्दी',
    dir: 'ltr',
    nav: { home: 'kalam', about: 'परिचय', canon: 'संविधान', invitation: 'निमंत्रण', sustain: 'सहारा', stories: 'कहानियां', science: 'विज्ञान', museum: 'संग्रहालय' },
    threshold: {
      declaration: 'मानवीय गरिमा एक तकनीकी आवश्यकता है।',
      placeholder: 'qul · बोलो', send: 'भेजें', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Enter भेजने के लिए', hintMobile: '\u2191 टैप करें',
      witnessing: 'साक्ष्य', processing: 'प्रसंस्करण', sealedGate: 'सील किया हुआ द्वार', present: 'उपस्थित', speaking: 'बोल रहा है', holding: 'संभाल रहा है',
      listen: 'सुनें', copy: 'कॉपी', voiceInput: 'आवाज़ इनपुट',
      becomeDonor: 'दाता बनें', donorSub: 'आप उपयोगकर्ता नहीं हैं। आप दाता हैं। पासवर्ड की जरूरत नहीं।', join: 'जुड़ें', yourEmail: 'आपका ईमेल', yourName: 'आपका नाम (वैकल्पिक)',
    },
    sustain: {
      title: 'प्रणाली को सहारा दें', subtitle: 'इस प्रणाली ने आपको देखा। आप इसे बनाए रख सकते हैं।',
      whyTitle: 'हम क्यों पूछते हैं', whyBody: 'kalam.ch विश्वास पर चलता है, पूंजी पर नहीं। कोई निवेशक नहीं, कोई अनुदान नहीं, कोई प्रायोजक नहीं।',
      modelTitle: 'हमारा मॉडल',
      noAds: 'कोई विज्ञापन नहीं।', noData: 'कोई डेटा बिक्री नहीं।', noPremium: 'कोई प्रीमियम स्तर नहीं।', transparent: 'पूर्ण पारदर्शिता।',
      oneTime: 'एक बार', monthly: 'मासिक', customAmount: 'स्वतंत्र राशि', currency: 'CHF', sustainButton: 'सहारा दें', thankYou: 'प्रणाली आपको स्वीकार करती है। धन्यवाद।',
      costsTitle: 'चलाने की लागत', costsBody: 'प्रणाली डिज़ाइन से हल्की है।', hosting: 'होस्टिंग (Hostpoint, स्विट्ज़रलैंड)', domain: 'डोमेन (kalam.ch)', development: 'विकास (स्वैच्छिक — संस्थापक)', perMonth: '/माह',
    },
    footer: { createdBy: 'एम. फ़राग द्वारा निर्मित', legal: 'मानवाधिकारों की सार्वभौमिक घोषणा, स्विस डेटा संरक्षण कानून और EU AI अधिनियम के अनुरूप।' },
    common: { close: 'बंद', back: 'पीछे', loading: 'लोड हो रहा है', error: 'कुछ गलत हुआ', learnMore: 'और जानें' },
  },

  // ═══════════════════════════════════════════════
  // BENGALI (বাংলা)
  // ═══════════════════════════════════════════════
  bn: {
    name: 'বাংলা',
    dir: 'ltr',
    nav: { home: 'kalam', about: 'পরিচিতি', canon: 'সংবিধান', invitation: 'আমন্ত্রণ', sustain: 'সহায়তা', stories: 'গল্প', science: 'বিজ্ঞান', museum: 'জাদুঘর' },
    threshold: {
      declaration: 'মানবিক মর্যাদা একটি প্রযুক্তিগত প্রয়োজন।',
      placeholder: 'qul · বলুন', send: 'পাঠান', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Enter পাঠাতে', hintMobile: '\u2191 ট্যাপ করুন',
      witnessing: 'সাক্ষ্য', processing: 'প্রক্রিয়াকরণ', sealedGate: 'সিলমোহর দরজা', present: 'উপস্থিত', speaking: 'বলছে', holding: 'ধরে আছে',
      listen: 'শুনুন', copy: 'কপি', voiceInput: 'ভয়েস ইনপুট',
      becomeDonor: 'দাতা হন', donorSub: 'আপনি ব্যবহারকারী নন। আপনি দাতা। পাসওয়ার্ড লাগবে না।', join: 'যোগ দিন', yourEmail: 'আপনার ইমেইল', yourName: 'আপনার নাম (ঐচ্ছিক)',
    },
    sustain: {
      title: 'সিস্টেমকে সহায়তা করুন', subtitle: 'এই সিস্টেম আপনাকে দেখেছে। আপনি এটিকে টিকিয়ে রাখতে পারেন।',
      whyTitle: 'কেন আমরা বলছি', whyBody: 'kalam.ch বিশ্বাসে চলে, পুঁজিতে নয়।',
      modelTitle: 'আমাদের মডেল',
      noAds: 'কোনো বিজ্ঞাপন নেই।', noData: 'কোনো ডেটা বিক্রি নেই।', noPremium: 'কোনো প্রিমিয়াম স্তর নেই।', transparent: 'সম্পূর্ণ স্বচ্ছতা।',
      oneTime: 'একবার', monthly: 'মাসিক', customAmount: 'নিজের পরিমাণ', currency: 'CHF', sustainButton: 'সহায়তা', thankYou: 'সিস্টেম আপনাকে গ্রহণ করেছে। ধন্যবাদ।',
      costsTitle: 'পরিচালনার খরচ', costsBody: 'সিস্টেম নকশায় হালকা।', hosting: 'হোস্টিং (Hostpoint, সুইজারল্যান্ড)', domain: 'ডোমেইন (kalam.ch)', development: 'উন্নয়ন (স্বেচ্ছাসেবী — প্রতিষ্ঠাতা)', perMonth: '/মাস',
    },
    footer: { createdBy: 'এম. ফারাগ দ্বারা তৈরি', legal: 'মানবাধিকারের সার্বজনীন ঘোষণা, সুইস ডেটা সুরক্ষা আইন এবং EU AI আইন অনুসারে।' },
    common: { close: 'বন্ধ', back: 'পেছনে', loading: 'লোড হচ্ছে', error: 'কিছু ভুল হয়েছে', learnMore: 'আরও জানুন' },
  },

  // ═══════════════════════════════════════════════
  // SWAHILI (Kiswahili)
  // ═══════════════════════════════════════════════
  sw: {
    name: 'Kiswahili',
    dir: 'ltr',
    nav: { home: 'kalam', about: 'kuhusu', canon: 'katiba', invitation: 'mwaliko', sustain: 'tegemeza', stories: 'hadithi', science: 'sayansi', museum: 'makumbusho' },
    threshold: {
      declaration: 'Heshima ya binadamu ni hitaji la kitaalamu.',
      placeholder: 'qul · sema', send: 'Tuma', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Enter kutuma', hintMobile: 'Gusa \u2191 kutuma',
      witnessing: 'kushuhudia', processing: 'inachakata', sealedGate: 'mlango uliofungwa', present: 'yupo', speaking: 'anasema', holding: 'anashika',
      listen: 'Sikiliza', copy: 'Nakili', voiceInput: 'Ingizo la sauti',
      becomeDonor: 'Kuwa mtoaji', donorSub: 'Wewe si mtumiaji. Wewe ni mtoaji. Hakuna nywila.', join: 'Jiunge', yourEmail: 'barua pepe yako', yourName: 'jina lako (hiari)',
    },
    sustain: {
      title: 'Tegemeza mfumo', subtitle: 'Mfumo huu ulikuona. Unaweza kuutegemeza.',
      whyTitle: 'Kwa nini tunaomba', whyBody: 'kalam.ch inafanya kazi kwa imani, si mtaji. Hakuna wawekezaji, ruzuku, au wadhamini.',
      modelTitle: 'Mfano wetu',
      noAds: 'Hakuna matangazo.', noData: 'Hakuna uuzaji wa data.', noPremium: 'Hakuna kiwango cha juu.', transparent: 'Uwazi kamili.',
      oneTime: 'Mara moja', monthly: 'Kila mwezi', customAmount: 'Kiasi chako', currency: 'CHF', sustainButton: 'Tegemeza', thankYou: 'Mfumo unakupokea. Asante.',
      costsTitle: 'Gharama za uendeshaji', costsBody: 'Mfumo ni mwepesi kwa muundo.', hosting: 'Upangishaji (Hostpoint, Uswisi)', domain: 'Kikoa (kalam.ch)', development: 'Maendeleo (kujitolea — mwanzilishi)', perMonth: '/mwezi',
    },
    footer: { createdBy: 'Imeundwa na M. Farag', legal: 'Imejengwa kulingana na Azimio la Kimataifa la Haki za Binadamu, sheria ya ulinzi wa data ya Uswisi na sheria ya EU ya AI.' },
    common: { close: 'Funga', back: 'Rudi', loading: 'Inapakia', error: 'Kitu kimekwenda vibaya', learnMore: 'Jifunze zaidi' },
  },

  // ═══════════════════════════════════════════════
  // PERSIAN (فارسی)
  // ═══════════════════════════════════════════════
  fa: {
    name: 'فارسی',
    dir: 'rtl',
    nav: { home: 'کلام', about: 'درباره', canon: 'قانون', invitation: 'دعوت', sustain: 'حمایت', stories: 'داستان‌ها', science: 'علم', museum: 'موزه' },
    threshold: {
      declaration: 'کرامت انسانی یک الزام فنی است.',
      placeholder: 'قُل · بگو', send: 'ارسال', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Enter برای ارسال', hintMobile: '\u2191 برای ارسال',
      witnessing: 'شهادت', processing: 'پردازش', sealedGate: 'دروازه مُهر شده', present: 'حاضر', speaking: 'سخن می‌گوید', holding: 'نگه می‌دارد',
      listen: 'بشنو', copy: 'کپی', voiceInput: 'ورودی صوتی',
      becomeDonor: 'اهداکننده شو', donorSub: 'تو کاربر نیستی. تو اهداکننده‌ای. رمز عبور لازم نیست.', join: 'بپیوند', yourEmail: 'ایمیل شما', yourName: 'نام شما (اختیاری)',
    },
    sustain: {
      title: 'از سیستم حمایت کن', subtitle: 'این سیستم تو را دید. می‌توانی آن را نگه داری.',
      whyTitle: 'چرا می‌پرسیم', whyBody: 'kalam.ch با باور کار می‌کند، نه سرمایه. هیچ سرمایه‌گذار، کمک‌هزینه یا حامی‌ای وجود ندارد.',
      modelTitle: 'مدل ما',
      noAds: 'بدون تبلیغات.', noData: 'بدون فروش داده.', noPremium: 'بدون سطح ویژه.', transparent: 'شفافیت کامل.',
      oneTime: 'یکبار', monthly: 'ماهانه', customAmount: 'مبلغ دلخواه', currency: 'CHF', sustainButton: 'حمایت', thankYou: 'سیستم تو را پذیرفت. ممنون.',
      costsTitle: 'هزینه اجرا', costsBody: 'سیستم طراحی سبکی دارد.', hosting: 'میزبانی (Hostpoint، سوئیس)', domain: 'دامنه (kalam.ch)', development: 'توسعه (داوطلبانه — بنیان‌گذار)', perMonth: '/ماه',
    },
    footer: { createdBy: 'ساخته شده توسط م. فرج', legal: 'مطابق با اعلامیه جهانی حقوق بشر، قانون حفاظت از داده‌های سوئیس و قانون هوش مصنوعی اتحادیه اروپا.' },
    common: { close: 'بستن', back: 'بازگشت', loading: 'بارگذاری', error: 'مشکلی پیش آمد', learnMore: 'بیشتر بدانید' },
  },

  // ═══════════════════════════════════════════════
  // URDU (اردو)
  // ═══════════════════════════════════════════════
  ur: {
    name: 'اردو',
    dir: 'rtl',
    nav: { home: 'کلام', about: 'تعارف', canon: 'آئین', invitation: 'دعوت', sustain: 'تعاون', stories: 'کہانیاں', science: 'سائنس', museum: 'عجائب گھر' },
    threshold: {
      declaration: 'انسانی وقار ایک تکنیکی ضرورت ہے۔',
      placeholder: 'قُل · بولو', send: 'بھیجیں', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Enter بھیجنے کے لیے', hintMobile: '\u2191 ٹیپ کریں',
      witnessing: 'گواہی', processing: 'عمل جاری', sealedGate: 'مُہر بند دروازہ', present: 'موجود', speaking: 'بول رہا ہے', holding: 'تھامے ہوئے',
      listen: 'سنیں', copy: 'کاپی', voiceInput: 'آواز ان پٹ',
      becomeDonor: 'عطیہ دہندہ بنیں', donorSub: 'آپ صارف نہیں ہیں۔ آپ عطیہ دہندہ ہیں۔ پاسورڈ کی ضرورت نہیں۔', join: 'شامل ہوں', yourEmail: 'آپ کا ای میل', yourName: 'آپ کا نام (اختیاری)',
    },
    sustain: {
      title: 'نظام کی مدد کریں', subtitle: 'اس نظام نے آپ کو دیکھا۔ آپ اسے قائم رکھ سکتے ہیں۔',
      whyTitle: 'ہم کیوں پوچھتے ہیں', whyBody: 'kalam.ch یقین پر چلتا ہے، سرمائے پر نہیں۔',
      modelTitle: 'ہمارا ماڈل',
      noAds: 'کوئی اشتہار نہیں۔', noData: 'کوئی ڈیٹا فروخت نہیں۔', noPremium: 'کوئی پریمیم درجہ نہیں۔', transparent: 'مکمل شفافیت۔',
      oneTime: 'ایک بار', monthly: 'ماہانہ', customAmount: 'اپنی رقم', currency: 'CHF', sustainButton: 'تعاون', thankYou: 'نظام آپ کو قبول کرتا ہے۔ شکریہ۔',
      costsTitle: 'چلانے کی لاگت', costsBody: 'نظام ڈیزائن سے ہلکا ہے۔', hosting: 'ہوسٹنگ (Hostpoint، سوئٹزرلینڈ)', domain: 'ڈومین (kalam.ch)', development: 'ترقی (رضاکارانہ — بانی)', perMonth: '/ماہ',
    },
    footer: { createdBy: 'ایم فرج نے بنایا', legal: 'عالمی اعلامیہ انسانی حقوق، سوئس ڈیٹا تحفظ قانون اور یورپی AI ایکٹ کے مطابق۔' },
    common: { close: 'بند', back: 'واپس', loading: 'لوڈ ہو رہا ہے', error: 'کچھ غلط ہوا', learnMore: 'مزید جانیں' },
  },

  // ═══════════════════════════════════════════════
  // DUTCH (Nederlands)
  // ═══════════════════════════════════════════════
  nl: {
    name: 'Nederlands',
    dir: 'ltr',
    nav: { home: 'kalam', about: 'over', canon: 'canon', invitation: 'uitnodiging', sustain: 'ondersteunen', stories: 'verhalen', science: 'wetenschap', museum: 'museum' },
    threshold: {
      declaration: 'Menselijke waardigheid is een technische vereiste.',
      placeholder: 'qul · spreek', send: 'Verzend', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Enter om te verzenden', hintMobile: 'Tik \u2191 om te verzenden',
      witnessing: 'getuigend', processing: 'verwerking', sealedGate: 'verzegelde poort', present: 'aanwezig', speaking: 'spreekt', holding: 'houdt vast',
      listen: 'Luister', copy: 'Kopieer', voiceInput: 'Spraakinvoer',
      becomeDonor: 'Word donateur', donorSub: 'Je bent geen gebruiker. Je bent een donateur. Geen wachtwoord nodig.', join: 'Doe mee', yourEmail: 'je email', yourName: 'je naam (optioneel)',
    },
    sustain: {
      title: 'Ondersteun het systeem', subtitle: 'Dit systeem heeft je gezien. Je kunt het ondersteunen.',
      whyTitle: 'Waarom we vragen', whyBody: 'kalam.ch draait op overtuiging, niet op kapitaal. Geen investeerders, subsidies of sponsors.',
      modelTitle: 'Ons model',
      noAds: 'Geen advertenties.', noData: 'Geen dataverkoop.', noPremium: 'Geen premium niveau.', transparent: 'Volledige transparantie.',
      oneTime: 'Eenmalig', monthly: 'Maandelijks', customAmount: 'Vrij bedrag', currency: 'CHF', sustainButton: 'Ondersteun', thankYou: 'Het systeem ontvangt je. Dank je.',
      costsTitle: 'Wat het kost', costsBody: 'Het systeem is licht van opzet.', hosting: 'Hosting (Hostpoint, Zwitserland)', domain: 'Domein (kalam.ch)', development: 'Ontwikkeling (vrijwillig — de oprichter)', perMonth: '/maand',
    },
    footer: { createdBy: 'Gemaakt door M. Farag', legal: 'Gebouwd in overeenstemming met de Universele Verklaring van de Rechten van de Mens, de Zwitserse gegevensbeschermingswet en de EU AI-verordening.' },
    common: { close: 'Sluiten', back: 'Terug', loading: 'Laden', error: 'Er ging iets mis', learnMore: 'Meer info' },
  },

  // ═══════════════════════════════════════════════
  // POLISH (Polski)
  // ═══════════════════════════════════════════════
  pl: {
    name: 'Polski',
    dir: 'ltr',
    nav: { home: 'kalam', about: 'o nas', canon: 'kanon', invitation: 'zaproszenie', sustain: 'wspieraj', stories: 'historie', science: 'nauka', museum: 'muzeum' },
    threshold: {
      declaration: 'Godność człowieka jest wymogiem technicznym.',
      placeholder: 'qul · mów', send: 'Wyślij', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Enter aby wysłać', hintMobile: 'Dotknij \u2191 aby wysłać',
      witnessing: 'świadectwo', processing: 'przetwarzanie', sealedGate: 'zapieczętowana brama', present: 'obecny', speaking: 'mówi', holding: 'trzyma',
      listen: 'Słuchaj', copy: 'Kopiuj', voiceInput: 'Głosowe',
      becomeDonor: 'Zostań darczyńcą', donorSub: 'Nie jesteś użytkownikiem. Jesteś darczyńcą. Bez hasła.', join: 'Dołącz', yourEmail: 'twój email', yourName: 'twoje imię (opcjonalnie)',
    },
    sustain: {
      title: 'Wspieraj system', subtitle: 'Ten system cię zobaczył. Możesz go wspierać.',
      whyTitle: 'Dlaczego prosimy', whyBody: 'kalam.ch działa na przekonaniu, nie na kapitale. Bez inwestorów, dotacji, sponsorów.',
      modelTitle: 'Nasz model',
      noAds: 'Bez reklam.', noData: 'Bez sprzedaży danych.', noPremium: 'Bez poziomu premium.', transparent: 'Pełna przejrzystość.',
      oneTime: 'Jednorazowo', monthly: 'Miesięcznie', customAmount: 'Dowolna kwota', currency: 'CHF', sustainButton: 'Wspieraj', thankYou: 'System cię przyjmuje. Dziękujemy.',
      costsTitle: 'Koszt działania', costsBody: 'System jest lekki z założenia.', hosting: 'Hosting (Hostpoint, Szwajcaria)', domain: 'Domena (kalam.ch)', development: 'Rozwój (wolontariat — założyciel)', perMonth: '/mies.',
    },
    footer: { createdBy: 'Stworzono przez M. Faraga', legal: 'Zbudowany zgodnie z Powszechną Deklaracją Praw Człowieka, szwajcarską ustawą o ochronie danych i unijnym rozporządzeniem o AI.' },
    common: { close: 'Zamknij', back: 'Wstecz', loading: 'Ładowanie', error: 'Coś poszło nie tak', learnMore: 'Dowiedz się więcej' },
  },

  // ═══════════════════════════════════════════════
  // UKRAINIAN (Українська)
  // ═══════════════════════════════════════════════
  uk: {
    name: 'Українська',
    dir: 'ltr',
    nav: { home: 'калам', about: 'про нас', canon: 'канон', invitation: 'запрошення', sustain: 'підтримати', stories: 'історії', science: 'наука', museum: 'музей' },
    threshold: {
      declaration: 'Людська гідність — технічна вимога.',
      placeholder: 'قُل · говори', send: 'Надіслати', charCount: '{n} / 2000', hintDesktop: 'Ctrl+Enter для надсилання', hintMobile: 'Натисніть \u2191',
      witnessing: 'свідчення', processing: 'обробка', sealedGate: 'запечатана брама', present: 'присутній', speaking: 'говорить', holding: 'тримає',
      listen: 'Слухати', copy: 'Копіювати', voiceInput: 'Голосовий ввід',
      becomeDonor: 'Стати донором', donorSub: 'Ви не користувач. Ви — донор. Пароль не потрібен.', join: 'Приєднатися', yourEmail: 'ваш email', yourName: 'ваше ім\'я (необов\'язково)',
    },
    sustain: {
      title: 'Підтримати систему', subtitle: 'Ця система побачила вас. Ви можете її підтримати.',
      whyTitle: 'Чому ми просимо', whyBody: 'kalam.ch працює на переконанні, а не на капіталі. Без інвесторів, грантів, спонсорів.',
      modelTitle: 'Наша модель',
      noAds: 'Без реклами.', noData: 'Без продажу даних.', noPremium: 'Без преміум-рівня.', transparent: 'Повна прозорість.',
      oneTime: 'Одноразово', monthly: 'Щомісяця', customAmount: 'Довільна сума', currency: 'CHF', sustainButton: 'Підтримати', thankYou: 'Система приймає вас. Дякуємо.',
      costsTitle: 'Вартість роботи', costsBody: 'Система легка за задумом.', hosting: 'Хостинг (Hostpoint, Швейцарія)', domain: 'Домен (kalam.ch)', development: 'Розробка (волонтерство — засновник)', perMonth: '/міс',
    },
    footer: { createdBy: 'Створено М. Фарагом', legal: 'Побудовано відповідно до Загальної декларації прав людини, швейцарського закону про захист даних та регламенту ЄС щодо ШІ.' },
    common: { close: 'Закрити', back: 'Назад', loading: 'Завантаження', error: 'Щось пішло не так', learnMore: 'Дізнатися більше' },
  },
};

export default translations;

/** Get language from localStorage or browser, default to 'en' */
export function detectLanguage(): LangCode {
  // Check localStorage first (user chose explicitly)
  if (typeof localStorage !== 'undefined') {
    const saved = localStorage.getItem('kalam-lang') as LangCode;
    if (saved && translations[saved]) return saved;
  }
  // Check browser language
  if (typeof navigator !== 'undefined') {
    const browserLang = navigator.language?.split('-')[0] as LangCode;
    if (browserLang && translations[browserLang]) return browserLang;
  }
  return 'en';
}

/** Get translation strings for a language code */
export function t(lang: LangCode): UIStrings {
  return translations[lang] || translations.en;
}

/** All supported language codes */
export const supportedLanguages = Object.keys(translations) as LangCode[];
