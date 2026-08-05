<template>
  <div class="min-h-screen bg-surface text-on-surface font-body-md overflow-x-hidden">
    <!-- Top Navigation -->
    <header
      class="w-full top-0 sticky z-50 border-b transition-all duration-300"
      :class="scrolled ? 'bg-surface/90 backdrop-blur-md shadow-md border-outline-variant' : 'bg-surface/0 border-transparent'"
    >
      <div class="flex justify-between items-center h-row-height-md max-w-7xl mx-auto px-container-margin">
        <div class="flex items-center gap-2 font-display-lg text-headline-lg font-bold text-primary dark:text-primary-fixed">
          <span class="relative flex h-2.5 w-2.5">
            <span class="animate-ping-slow absolute inline-flex h-full w-full rounded-full bg-primary opacity-60"></span>
            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-primary"></span>
          </span>
          MYFBRPOS
        </div>
        <nav class="hidden md:flex items-center gap-8">
          <a class="nav-link" href="#" @click.prevent="goToDocs">Docs</a>
          <a class="nav-link" href="#" @click.prevent="scrollToAbout">About Us</a>
          <a class="nav-link" href="#" @click.prevent="scrollToFooter">Contact Us</a>
        </nav>
        <div class="flex items-center gap-3">
          <a class="font-title-md text-title-md text-on-surface-variant hover:bg-surface-container-low transition-all px-4 py-2 rounded-lg cursor-pointer" @click="$router.push('/login')">Login</a>
          <button class="btn-shine bg-primary text-on-primary px-6 py-2 rounded-lg font-title-md text-title-md shadow-md hover:shadow-lg hover:-translate-y-0.5 transition-all" @click="showBookDemoModal = true">
            Book a Demo
          </button>
        </div>
      </div>
    </header>

    <main>
      <!-- Hero Section -->
      <section class="relative pt-24 pb-32 overflow-hidden bg-mesh">
        <div class="blob blob-a"></div>
        <div class="blob blob-b"></div>

        <div class="max-w-7xl mx-auto px-container-margin grid grid-cols-1 lg:grid-cols-2 gap-12 items-center relative">
          <div class="z-10 hero-in">
            <div class="inline-flex items-center gap-2 bg-primary-container/10 border border-primary-container/20 px-3 py-1 rounded-full mb-6 badge-pop">
              <span class="material-symbols-outlined text-primary text-sm" style="font-variation-settings: 'FILL' 1;">verified</span>
              <span class="text-primary font-label-sm text-label-sm uppercase tracking-wider">FBR Tier-1 Licensed Partner</span>
            </div>
            <h1 class="font-display-lg text-display-lg text-on-surface leading-tight mb-4 hero-in hero-delay-1">
              FBR Compliance Made <span class="text-gradient">Simple</span> for Pakistani Businesses.
            </h1>
            <h2 class="font-headline-lg text-headline-lg text-primary font-bold mb-6 hero-in hero-delay-2">
              No More Manual Filing. No More Guesswork.
            </h2>
            <p class="font-body-lg text-body-lg text-on-surface-variant mb-10 max-w-xl hero-in hero-delay-3">
              From barcode scanning to FBR-verified digital receipts, MYFBRPOS runs your entire storefront — invoicing, inventory, and tax compliance — in one place. Every sale is submitted to FBR in real time and backed by a 6-year audit trail, so you stay compliant without lifting a finger. Trusted by 500+ retailers across Pakistan.
            </p>
            <div class="flex flex-col sm:flex-row gap-4 hero-in hero-delay-4">
              <button @click="scrollToAutomate" class="btn-shine bg-primary text-on-primary px-8 py-4 rounded-xl font-title-md text-title-md shadow-lg shadow-primary/20 hover:scale-[1.02] transition-transform">
                Automate Your Business
              </button>
              <button class="group flex items-center justify-center gap-2 border-2 border-primary text-primary px-8 py-4 rounded-xl font-title-md text-title-md hover:bg-primary/5 transition-colors">
                <span class="relative flex items-center justify-center w-6 h-6">
                  <span class="absolute inline-flex h-full w-full rounded-full bg-primary/20 group-hover:animate-ping-slow"></span>
                  <span class="material-symbols-outlined relative text-2xl">play_circle</span>
                </span>
                Watch Demo
              </button>
            </div>
          </div>

          <div class="relative hero-in hero-delay-2">
            <div class="absolute -top-12 -right-12 w-64 h-64 bg-primary/10 blur-3xl rounded-full float-slow"></div>
            <div class="bg-white p-4 rounded-2xl shadow-2xl border border-outline-variant relative z-10 hover:shadow-primary/10 hover:-translate-y-1 transition-all duration-500">
              <img
                class="w-full h-auto rounded-xl"
                alt="Dashboard preview showing sales trends, inventory levels, and a live FBR submission status panel"
                src="https://lh3.googleusercontent.com/aida-public/AB6AXuBy_XtFfPSEpY0587YlPjLE7deXg2UJpz6Dk-ktWbi6TAb57g3yOKNWXePHw6m1EPdVAxnUxk_b0_bk60KVfB0nNabywFhwNwRjgxH9qWXJyOL6y4YDvko28HEJY10gKFnyBDQSgJqHOeTj2WAkOFiv93dsUYi2iJbfUa4ZXnkVnv8vTQ5YuY5KSnTIFlKPUNukw2MlBt_ad_kf5kjwX0KOT6_ytmVd7_Cjnui6t-p-9o4KFCUo8L8n"
              />
              <div class="absolute -bottom-6 -left-6 bg-white p-4 rounded-xl shadow-xl border border-outline-variant flex items-center gap-4 animate-bounce-slow">
                <div class="w-12 h-12 bg-primary/10 rounded-full flex items-center justify-center text-primary">
                  <span class="material-symbols-outlined" style="font-variation-settings: 'FILL' 1;">qr_code_2</span>
                </div>
                <div>
                  <div class="text-label-sm font-label-sm text-text-muted">Live Receipt</div>
                  <div class="text-body-md font-bold text-primary flex items-center gap-1">
                    FBR Verified
                    <span class="relative flex h-2 w-2">
                      <span class="animate-ping-slow absolute inline-flex h-full w-full rounded-full bg-primary opacity-70"></span>
                      <span class="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Trust Bar -->
      <section class="bg-white border-y border-outline-variant py-10">
        <div class="max-w-7xl mx-auto px-container-margin">
          <div class="flex flex-wrap justify-between items-center gap-8 md:gap-12">
            <div class="flex items-center gap-3 trust-item reveal-up" v-for="(item, i) in trustBar" :key="item.label" :style="{ transitionDelay: i * 80 + 'ms' }">
              <span class="w-10 h-10 rounded-full bg-primary/10 flex items-center justify-center text-primary trust-icon">
                <span class="material-symbols-outlined text-2xl">{{ item.icon }}</span>
              </span>
              <span class="font-title-md text-title-md text-on-surface-variant">{{ item.label }}</span>
            </div>
          </div>
        </div>
      </section>

      <!-- Stats Strip (signature element) -->
      <section ref="statsSection" class="bg-primary py-14">
        <div class="max-w-7xl mx-auto px-container-margin grid grid-cols-2 md:grid-cols-4 gap-8 text-center">
          <div v-for="stat in stats" :key="stat.label">
            <div class="font-display-lg text-headline-lg text-white font-bold">
              {{ statsVisible ? stat.prefix + Math.round(stat.animated) + stat.suffix : stat.prefix + '0' + stat.suffix }}
            </div>
            <div class="text-white/70 font-label-sm text-label-sm uppercase tracking-wider mt-2">{{ stat.label }}</div>
          </div>
        </div>
      </section>

      <!-- Core Features -->
      <section class="py-24 bg-surface">
        <div class="max-w-7xl mx-auto px-container-margin">
          <div class="text-center mb-16 reveal-up">
            <h2 class="font-headline-lg text-headline-lg text-on-surface mb-4">Enterprise Features, Small Business Ease</h2>
            <p class="text-on-surface-variant max-w-2xl mx-auto">Everything you need to run your business legally and efficiently in Pakistan's evolving tax landscape.</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div
              v-for="(feature, i) in features"
              :key="feature.title"
              class="bento-card reveal-up bg-white p-8 rounded-2xl border border-outline-variant flex flex-col items-start h-full"
              :style="{ transitionDelay: i * 90 + 'ms' }"
            >
              <div class="w-12 h-12 bg-primary/10 rounded-lg flex items-center justify-center text-primary mb-6 feature-icon">
                <span class="material-symbols-outlined text-3xl">{{ feature.icon }}</span>
              </div>
              <h3 class="font-title-md text-title-md mb-3">{{ feature.title }}</h3>
              <p class="text-body-md text-on-surface-variant mb-6">{{ feature.description }}</p>
              <div class="mt-auto pt-4 border-t border-outline-variant w-full">
                <span class="text-label-sm font-label-sm text-primary flex items-center gap-1">
                  {{ feature.tag }} <span class="material-symbols-outlined text-xs">{{ feature.tagIcon }}</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Pakistan Specific Benefits -->
      <section class="py-24 bg-white relative">
        <div class="max-w-7xl mx-auto px-container-margin">
          <div class="bg-primary/5 rounded-3xl p-8 lg:p-16 flex flex-col lg:flex-row items-center gap-12 border border-primary/10 overflow-hidden relative reveal-up">
            <div class="absolute top-0 right-0 p-8 opacity-10">
              <span class="material-symbols-outlined text-9xl">public</span>
            </div>
            <div class="flex-1 space-y-8 z-10">
              <h2 class="font-headline-lg text-headline-lg text-primary">Tailored for the Pakistani Market</h2>
              <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div class="flex gap-4 benefit-item" v-for="point in localBenefits" :key="point.title">
                  <div class="shrink-0 w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center">
                    <span class="material-symbols-outlined text-sm">check</span>
                  </div>
                  <div>
                    <h4 class="font-title-md text-title-md mb-1">{{ point.title }}</h4>
                    <p class="text-body-md text-on-surface-variant">{{ point.description }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Customer Reviews Section -->
      <section class="py-24 bg-surface">
        <div class="max-w-7xl mx-auto px-container-margin">
          <div class="text-center mb-16 reveal-up">
            <h2 class="font-headline-lg text-headline-lg text-on-surface mb-4">Trusted by Pakistani Businesses</h2>
            <p class="text-on-surface-variant max-w-2xl mx-auto">See what our customers say about MYFBRPOS</p>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div
              v-for="(review, i) in reviews"
              :key="review.name"
              class="reveal-up bg-white p-10 rounded-2xl border border-outline-variant flex flex-col relative overflow-hidden hover:-translate-y-1 hover:shadow-xl transition-all duration-300"
              :style="{ transitionDelay: i * 100 + 'ms' }"
            >
              <span class="material-symbols-outlined absolute -top-2 -right-2 text-9xl text-primary/5 select-none">format_quote</span>
              <div class="flex items-center gap-1 mb-4 relative z-10">
                <span class="material-symbols-outlined text-primary text-xl star-pop" v-for="n in 5" :key="n" :style="{ animationDelay: (i * 100 + n * 60) + 'ms' }" style="font-variation-settings: 'FILL' 1;">star</span>
              </div>
              <p class="text-body-md text-on-surface-variant mb-6 flex-1 relative z-10">"{{ review.quote }}"</p>
              <div class="flex items-center gap-4 relative z-10">
                <div class="w-12 h-12 rounded-full flex items-center justify-center text-white font-bold avatar-ring">{{ review.initials }}</div>
                <div>
                  <div class="font-title-md text-title-md">{{ review.name }}</div>
                  <div class="text-label-sm text-text-muted">{{ review.role }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- About Us (now inline, was previously a modal) -->
      <section ref="aboutSection" class="py-24 bg-white border-t border-outline-variant scroll-mt-24">
        <div class="max-w-5xl mx-auto px-container-margin">
          <div class="text-center mb-14 reveal-up">
            <div class="inline-flex items-center gap-2 bg-primary/10 px-3 py-1 rounded-full mb-4">
              <span class="material-symbols-outlined text-primary text-sm">info</span>
              <span class="text-primary font-label-sm text-label-sm uppercase tracking-wider">About Us</span>
            </div>
            <h2 class="font-headline-lg text-headline-lg text-on-surface mb-4">About MYFBRPOS</h2>
            <p class="text-on-surface-variant max-w-2xl mx-auto">Pakistan's leading FBR-compliant Point of Sale system, built for Pakistani businesses.</p>
          </div>

          <div class="grid grid-cols-1 lg:grid-cols-2 gap-10 items-start">
            <div class="space-y-6 text-body-md reveal-up">
              <p>Since 2018, we have been helping retailers, wholesalers, and service providers automate their invoicing while ensuring full compliance with FBR regulations.</p>
              <p>Our platform integrates directly with the FBR's PRAL system, providing real-time invoice submission and verification. Every invoice you generate is automatically sent to FBR with a verifiable QR code, eliminating manual data entry and reducing compliance risks.</p>
              <p>We provide end-to-end solutions including software implementation, staff training, ongoing technical support, and compliance consulting. Our team is available 24/7 to assist with any issues or questions. With offices in Karachi, Lahore, and Islamabad, we offer on-site support across Pakistan.</p>
            </div>

            <div class="bg-primary/5 rounded-2xl p-8 border border-primary/10 reveal-up">
              <h4 class="font-title-md text-title-md mb-4 flex items-center gap-2">
                <span class="material-symbols-outlined text-primary">checklist</span> What We Offer
              </h4>
              <ul class="space-y-3">
                <li class="flex items-start gap-3 offer-item" v-for="(item, i) in aboutOffers" :key="item" :style="{ transitionDelay: i * 70 + 'ms' }">
                  <span class="shrink-0 w-6 h-6 rounded-full bg-primary text-white flex items-center justify-center mt-0.5">
                    <span class="material-symbols-outlined text-xs">check</span>
                  </span>
                  <span class="text-body-md text-on-surface-variant">{{ item }}</span>
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      <!-- Automate Your Business (now inline, was previously a modal) -->
      <section ref="automateSection" class="py-24 bg-surface border-t border-outline-variant scroll-mt-24">
        <div class="max-w-3xl mx-auto px-container-margin">
          <div class="text-center mb-12 reveal-up">
            <div class="inline-flex items-center gap-2 bg-primary/10 px-3 py-1 rounded-full mb-4">
              <span class="material-symbols-outlined text-primary text-sm">rocket_launch</span>
              <span class="text-primary font-label-sm text-label-sm uppercase tracking-wider">Get Started</span>
            </div>
            <h2 class="font-headline-lg text-headline-lg text-on-surface mb-4">Automate Your Business</h2>
            <p class="text-on-surface-variant max-w-xl mx-auto">Tell us a bit about your business and we'll set everything up for FBR-compliant selling.</p>
          </div>

          <div class="bg-white rounded-2xl border border-outline-variant p-8 lg:p-10 shadow-lg reveal-up">
            <template v-if="!automateSuccess">
              <form @submit.prevent="submitAutomateBusiness">
                <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div class="field-group">
                    <label class="field-label">Business Name</label>
                    <div class="field-with-icon">
                      <span class="material-symbols-outlined field-icon">storefront</span>
                      <input v-model="automateBusinessForm.business_name" type="text" required class="field-input" placeholder="e.g. Al-Noor Traders">
                    </div>
                  </div>
                  <div class="field-group">
                    <label class="field-label">Contact Name</label>
                    <div class="field-with-icon">
                      <span class="material-symbols-outlined field-icon">person</span>
                      <input v-model="automateBusinessForm.contact_name" type="text" class="field-input" placeholder="Your name">
                    </div>
                  </div>
                  <div class="field-group">
                    <label class="field-label">Email</label>
                    <div class="field-with-icon">
                      <span class="material-symbols-outlined field-icon">mail</span>
                      <input v-model="automateBusinessForm.email" type="email" required class="field-input" placeholder="you@business.com">
                    </div>
                  </div>
                  <div class="field-group">
                    <label class="field-label">Phone Number</label>
                    <div class="field-with-icon">
                      <span class="material-symbols-outlined field-icon">call</span>
                      <input v-model="automateBusinessForm.phone" type="tel" required class="field-input" placeholder="03XX-XXXXXXX">
                    </div>
                  </div>
                  <div class="field-group sm:col-span-2">
                    <label class="field-label">CNIC</label>
                    <div class="field-with-icon">
                      <span class="material-symbols-outlined field-icon">badge</span>
                      <input v-model="automateBusinessForm.cnic" type="text" required class="field-input" placeholder="XXXXX-XXXXXXX-X">
                    </div>
                  </div>
                  <div class="field-group sm:col-span-2">
                    <label class="field-label">Address</label>
                    <textarea v-model="automateBusinessForm.address" rows="2" class="field-input" placeholder="Shop / office address"></textarea>
                  </div>
                  <div class="field-group sm:col-span-2">
                    <label class="field-label">Message (Optional)</label>
                    <textarea v-model="automateBusinessForm.message" rows="3" class="field-input" placeholder="Tell us about your business, number of branches, or anything else"></textarea>
                  </div>
                </div>
                <button type="submit" :disabled="submitting" class="btn-shine w-full mt-6 bg-primary text-on-primary px-6 py-3 rounded-lg font-title-md hover:opacity-90 transition-all disabled:opacity-50 flex items-center justify-center gap-2">
                  <span v-if="submitting" class="spinner"></span>
                  {{ submitting ? 'Submitting...' : 'Get Started' }}
                </button>
              </form>
            </template>

            <template v-else>
              <div class="success-state">
                <div class="success-check"><span class="material-symbols-outlined">check</span></div>
                <h3 class="font-headline-lg text-headline-lg mb-2">You're All Set!</h3>
                <p class="text-body-md text-on-surface-variant">Our team will contact you shortly to get your business automated.</p>
              </div>
            </template>
          </div>
        </div>
      </section>

      <!-- Final CTA -->
      <section class="py-24 cta-gradient text-on-primary text-center relative overflow-hidden">
        <div class="blob blob-c"></div>
        <div class="max-w-4xl mx-auto px-container-margin relative z-10 reveal-up">
          <h2 class="font-display-lg text-headline-lg mb-6">Stay Compliant. Save Time. Grow Your Business.</h2>
          <p class="font-body-lg text-body-lg mb-10 opacity-90">Join 500+ Pakistani retailers who trust MYFBRPOS for their daily operations and tax reporting.</p>
          <div class="flex flex-col sm:flex-row justify-center gap-4">
            <button @click="scrollToAutomate" class="btn-shine bg-white text-primary px-10 py-4 rounded-xl font-title-md text-title-md shadow-xl hover:scale-[1.02] transition-all">
              Automate Your Business
            </button>
            <button @click="showContactModal = true" class="group relative flex items-center justify-center gap-2 bg-white/10 backdrop-blur-sm border-2 border-white/40 hover:border-white text-white px-10 py-4 rounded-xl font-title-md text-title-md transition-all overflow-hidden">
              <span class="absolute inset-0 bg-white/10 scale-0 group-hover:scale-100 transition-transform duration-500 rounded-xl"></span>
              <span class="material-symbols-outlined relative z-10">chat_bubble</span>
              <span class="relative z-10">Talk to Us</span>
            </button>
          </div>
        </div>
      </section>
    </main>

    <!-- Footer -->
    <footer ref="siteFooter" class="w-full py-12 bg-surface-container-highest dark:bg-inverse-surface border-t border-outline-variant scroll-mt-24">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-gutter max-w-7xl mx-auto px-container-margin">
        <div class="space-y-6">
          <div class="font-headline-lg text-headline-lg text-primary dark:text-primary-fixed">MYFBRPOS</div>
          <p class="font-body-md text-body-md text-on-surface-variant dark:text-surface-variant max-w-xs">
            Pakistan's most trusted FBR-certified POS solution provider. Simplifying retail compliance since 2018.
          </p>
        </div>
        <div class="grid grid-cols-2 gap-8">
          <div>
            <h4 class="font-title-md text-on-surface dark:text-inverse-on-surface mb-6">Company</h4>
            <ul class="space-y-4">
              <li><a class="footer-link" @click="scrollToAbout">About Us</a></li>
            </ul>
          </div>
          <div>
            <h4 class="font-title-md text-on-surface dark:text-inverse-on-surface mb-6">Resources</h4>
            <ul class="space-y-4">
              <li><a class="footer-link" @click.prevent="goToDocs">Docs</a></li>
              <li><a class="footer-link" @click.prevent="scrollToFooter">Contact Us</a></li>
            </ul>
          </div>
        </div>
        <div class="space-y-6 contact-highlight-wrap rounded-2xl transition-all duration-500" :class="{ 'contact-highlight': contactHighlight }">
          <h4 class="font-title-md text-on-surface dark:text-inverse-on-surface mb-6">Contact</h4>
          <div class="flex flex-col gap-4">
            <a class="footer-link flex items-center gap-2" href="mailto:myfbrpos@gmail.com">
              <span class="material-symbols-outlined text-lg text-primary">mail</span>myfbrpos@gmail.com
            </a>
            <a class="footer-link flex items-center gap-2" href="https://wa.me/923150498017">
              <span class="material-symbols-outlined text-lg text-primary">chat</span>03150498017 (WhatsApp)
            </a>
          </div>
          <div class="text-label-sm font-label-sm text-text-muted mt-10">
            © 2024 MYFBRPOS. All rights reserved. FBR Integrated POS Solutions.
          </div>
        </div>
      </div>
    </footer>

    <!-- Book Demo Modal -->
    <Transition name="modal">
      <div v-if="showBookDemoModal" class="modal-backdrop" @click.self="closeBookDemo">
        <div class="modal-card">
          <button @click="closeBookDemo" class="modal-close absolute top-6 right-6"><span class="material-symbols-outlined">close</span></button>

          <template v-if="!bookDemoSuccess">
            <div class="modal-banner">
              <span class="modal-banner-icon"><span class="material-symbols-outlined">calendar_month</span></span>
              <div>
                <h3 class="font-headline-lg text-headline-lg leading-tight">Book a Demo</h3>
                <p class="text-body-md text-on-surface-variant">See MYFBRPOS in action, tailored to your business.</p>
              </div>
            </div>
            <form @submit.prevent="submitBookDemo">
              <div class="space-y-4">
                <div class="field-group">
                  <label class="field-label">Business Name</label>
                  <div class="field-with-icon">
                    <span class="material-symbols-outlined field-icon">storefront</span>
                    <input v-model="bookDemoForm.business_name" type="text" required class="field-input" placeholder="e.g. Al-Noor Traders">
                  </div>
                </div>
                <div class="field-group">
                  <label class="field-label">Email</label>
                  <div class="field-with-icon">
                    <span class="material-symbols-outlined field-icon">mail</span>
                    <input v-model="bookDemoForm.email" type="email" required class="field-input" placeholder="you@business.com">
                  </div>
                </div>
                <div class="field-group">
                  <label class="field-label">Phone Number</label>
                  <div class="field-with-icon">
                    <span class="material-symbols-outlined field-icon">call</span>
                    <input v-model="bookDemoForm.phone" type="tel" required class="field-input" placeholder="03XX-XXXXXXX">
                  </div>
                </div>
                <div class="field-group">
                  <label class="field-label">Message (Optional)</label>
                  <textarea v-model="bookDemoForm.message" rows="3" class="field-input" placeholder="Anything specific you'd like the demo to cover?"></textarea>
                </div>
              </div>
              <button type="submit" :disabled="submitting" class="btn-shine w-full mt-6 bg-primary text-on-primary px-6 py-3 rounded-lg font-title-md hover:opacity-90 transition-all disabled:opacity-50 flex items-center justify-center gap-2">
                <span v-if="submitting" class="spinner"></span>
                {{ submitting ? 'Submitting...' : 'Request Demo' }}
              </button>
            </form>
          </template>

          <template v-else>
            <div class="success-state">
              <div class="success-check"><span class="material-symbols-outlined">check</span></div>
              <h3 class="font-headline-lg text-headline-lg mb-2">Demo Requested!</h3>
              <p class="text-body-md text-on-surface-variant">We'll reach out shortly to schedule your walkthrough.</p>
            </div>
          </template>
        </div>
      </div>
    </Transition>

    <!-- Contact Modal -->
    <Transition name="modal">
      <div v-if="showContactModal" class="modal-backdrop" @click.self="showContactModal = false">
        <div class="modal-card">
          <div class="flex justify-between items-center mb-6">
            <h3 class="font-headline-lg text-headline-lg">Contact Us</h3>
            <button @click="showContactModal = false" class="modal-close"><span class="material-symbols-outlined">close</span></button>
          </div>
          <div class="space-y-4">
            <a href="mailto:myfbrpos@gmail.com" class="contact-row">
              <div class="contact-icon"><span class="material-symbols-outlined">email</span></div>
              <div>
                <div class="text-label-sm text-text-muted">Email</div>
                <div class="text-body-md font-medium">myfbrpos@gmail.com</div>
              </div>
            </a>
            <a href="https://wa.me/923150498017" class="contact-row">
              <div class="contact-icon"><span class="material-symbols-outlined">phone</span></div>
              <div>
                <div class="text-label-sm text-text-muted">WhatsApp</div>
                <div class="text-body-md font-medium">03150498017</div>
              </div>
            </a>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, onUnmounted } from 'vue'
import { publicAPI } from '@/apis/public/publicAPI'

/* ---------------- Modal state ---------------- */
const showBookDemoModal = ref(false)
const showContactModal = ref(false)
const submitting = ref(false)
const bookDemoSuccess = ref(false)
const automateSuccess = ref(false)

const closeBookDemo = () => { showBookDemoModal.value = false; bookDemoSuccess.value = false }

/* ---------------- Header scroll effect ---------------- */
const scrolled = ref(false)
const onScroll = () => { scrolled.value = window.scrollY > 20 }

/* ---------------- Contact Us -> jump to footer ---------------- */
const siteFooter = ref<HTMLElement | null>(null)
const contactHighlight = ref(false)
const scrollToFooter = () => {
  siteFooter.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
  contactHighlight.value = true
  setTimeout(() => { contactHighlight.value = false }, 1600)
}

/* ---------------- About Us -> now an inline section, scroll to it ---------------- */
const aboutSection = ref<HTMLElement | null>(null)
const scrollToAbout = () => {
  aboutSection.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

/* ---------------- Automate Your Business -> now an inline section, scroll to it ---------------- */
const automateSection = ref<HTMLElement | null>(null)
const scrollToAutomate = () => {
  automateSection.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

const goToDocs = () => {
  window.location.href = '/docs'
}

/* ---------------- Content data ---------------- */
const trustBar = [
  { icon: 'account_balance', label: 'Integrated with PRAL/FBR' },
  { icon: 'receipt_long', label: 'Handles all 28 Tax Scenarios' },
  { icon: 'history_edu', label: '6-Year Audit Trail' },
  { icon: 'support_agent', label: 'Local 24/7 Support' },
]

const features = [
  { icon: 'send_and_archive', title: 'Automatic FBR Submission', description: 'Real-time integration with FBR servers. Every invoice generates a verifiable QR code instantly.', tag: 'Zero Latency', tagIcon: 'bolt' },
  { icon: 'point_of_sale', title: 'Complete POS System', description: 'Support for barcodes, thermal printers, and split payment methods (Cash/Card/Wallet).', tag: 'Hardware Agnostic', tagIcon: 'settings_input_component' },
  { icon: 'domain', title: 'Multi-Location Support', description: 'Manage inventory and sales across 50+ branches from a single cloud-based dashboard.', tag: 'Cloud Sync', tagIcon: 'cloud_done' },
  { icon: 'inventory_2', title: 'Inventory & Customers', description: 'Low stock alerts, NTN tracking for registered buyers, and automated reordering.', tag: 'CRM Integrated', tagIcon: 'group' },
]

const localBenefits = [
  { title: 'HS Code Integration', description: 'Full database of HS codes for easy classification of imported items in accordance with customs laws.' },
  { title: 'Tax Status Verification', description: 'Live NTN verification for registered vs unregistered buyer tracking to ensure accurate withholding tax.' },
  { title: 'Local POS Standards', description: 'Supports Annexure-C and other local filing formats for smooth monthly reporting with your tax consultant.' },
  { title: '24/7 Local Support', description: 'On-site support in Karachi, Lahore, and Islamabad, plus Urdu/English phone assistance.' },
]

const reviews = [
  { initials: 'AK', name: 'Ahmed Khan', role: 'Retail Store Owner, Karachi', quote: 'MYFBRPOS has completely transformed our business operations. The FBR integration is seamless and the support team is always available.' },
  { initials: 'SA', name: 'Sara Ahmed', role: 'Clothing Boutique, Lahore', quote: 'The automated FBR submission saves us hours every week. No more manual data entry or worrying about compliance issues.' },
  { initials: 'MR', name: 'Muhammad Riaz', role: 'Electronics Store, Islamabad', quote: 'Excellent customer support and the system is very easy to use. Highly recommend for any business needing FBR compliance.' },
]

const aboutOffers = [
  'Complete POS system with inventory management',
  'Automatic FBR invoice submission and QR code generation',
  'Support for all 28 FBR tax scenarios',
  'Multi-location management for growing businesses',
  'Customer relationship management (CRM)',
  'Detailed reporting and analytics',
  '6-year audit trail for compliance',
]

/* ---------------- Stats count-up (signature moment) ---------------- */
const statsSection = ref<HTMLElement | null>(null)
const statsVisible = ref(false)
const stats = reactive([
  { label: 'Businesses Automated', target: 500, animated: 0, prefix: '', suffix: '+' },
  { label: 'Tax Scenarios Covered', target: 28, animated: 0, prefix: '', suffix: '' },
  { label: 'Year Audit Trail', target: 6, animated: 0, prefix: '', suffix: '-Yr' },
  { label: 'Support & Assistance', target: 24, animated: 0, prefix: '', suffix: '/7' },
])

function animateStats() {
  const duration = 1400
  const start = performance.now()
  function tick(now: number) {
    const progress = Math.min((now - start) / duration, 1)
    const eased = 1 - Math.pow(1 - progress, 3)
    stats.forEach(s => { s.animated = s.target * eased })
    if (progress < 1) requestAnimationFrame(tick)
  }
  requestAnimationFrame(tick)
}

let statsObserver: IntersectionObserver | null = null
let revealObserver: IntersectionObserver | null = null

onMounted(() => {
  window.addEventListener('scroll', onScroll, { passive: true })

  if (statsSection.value) {
    statsObserver = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting && !statsVisible.value) {
          statsVisible.value = true
          animateStats()
          statsObserver?.disconnect()
        }
      })
    }, { threshold: 0.3 })
    statsObserver.observe(statsSection.value)
  }

  revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-in')
        revealObserver?.unobserve(entry.target)
      }
    })
  }, { threshold: 0.15 })
  document.querySelectorAll('.reveal-up, .trust-item, .benefit-item, .offer-item').forEach(el => revealObserver?.observe(el))
})

onUnmounted(() => {
  window.removeEventListener('scroll', onScroll)
  statsObserver?.disconnect()
  revealObserver?.disconnect()
})

/* ---------------- Forms ---------------- */
const bookDemoForm = ref({
  lead_type: 'demo_request' as const,
  business_name: '',
  email: '',
  phone: '',
  message: ''
})

const automateBusinessForm = ref({
  lead_type: 'business_automation' as const,
  business_name: '',
  contact_name: '',
  email: '',
  phone: '',
  cnic: '',
  address: '',
  message: ''
})

const submitBookDemo = async () => {
  submitting.value = true
  try {
    await publicAPI.submitLead(bookDemoForm.value)
    bookDemoSuccess.value = true
    bookDemoForm.value = { lead_type: 'demo_request', business_name: '', email: '', phone: '', message: '' }
    setTimeout(closeBookDemo, 2200)
  } catch (error) {
    alert('Failed to submit. Please try again.')
  } finally {
    submitting.value = false
  }
}

const submitAutomateBusiness = async () => {
  submitting.value = true
  try {
    await publicAPI.submitLead(automateBusinessForm.value)
    automateSuccess.value = true
    automateBusinessForm.value = { lead_type: 'business_automation', business_name: '', contact_name: '', email: '', phone: '', cnic: '', address: '', message: '' }
    // Since this is now an inline section (not a modal), reset back to the
    // empty form after a while so the person can submit again if needed.
    setTimeout(() => { automateSuccess.value = false }, 4000)
  } catch (error) {
    alert('Failed to submit. Please try again.')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
/* ---------- Background & ambient motion ---------- */
.bg-mesh {
  background-color: #f9f9ff;
  background-image: radial-gradient(at 0% 0%, rgba(0, 128, 128, 0.06) 0px, transparent 50%),
                    radial-gradient(at 100% 100%, rgba(0, 128, 128, 0.06) 0px, transparent 50%);
}

.blob {
  position: absolute;
  border-radius: 9999px;
  filter: blur(60px);
  opacity: 0.35;
  pointer-events: none;
  z-index: 0;
}
.blob-a { width: 380px; height: 380px; background: var(--primary-fixed); top: -120px; left: -100px; animation: drift 16s ease-in-out infinite; }
.blob-b { width: 300px; height: 300px; background: var(--primary); top: 40%; right: -120px; opacity: 0.12; animation: drift 20s ease-in-out infinite reverse; }
.blob-c { width: 420px; height: 420px; background: white; opacity: 0.08; top: -160px; right: -100px; position: absolute; animation: drift 18s ease-in-out infinite; }

@keyframes drift {
  0%, 100% { transform: translate(0, 0) scale(1); }
  50% { transform: translate(20px, 30px) scale(1.08); }
}

/* ---------- Hero entrance sequence ---------- */
.hero-in {
  opacity: 0;
  transform: translateY(18px);
  animation: hero-rise 0.7s cubic-bezier(0.22, 1, 0.36, 1) forwards;
}
.hero-delay-1 { animation-delay: 0.08s; }
.hero-delay-2 { animation-delay: 0.16s; }
.hero-delay-3 { animation-delay: 0.24s; }
.hero-delay-4 { animation-delay: 0.32s; }
@keyframes hero-rise {
  to { opacity: 1; transform: translateY(0); }
}

.badge-pop {
  animation: badge-pop 0.5s cubic-bezier(0.34, 1.56, 0.64, 1) 0.05s both;
}
@keyframes badge-pop {
  0% { opacity: 0; transform: scale(0.85); }
  100% { opacity: 1; transform: scale(1); }
}

.float-slow { animation: float-slow 6s ease-in-out infinite; }
@keyframes float-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-14px); }
}

/* ---------- Text gradient ---------- */
.text-gradient {
  background: linear-gradient(90deg, var(--primary), var(--primary-container));
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.cta-gradient {
  background: linear-gradient(135deg, var(--primary), var(--surface-tint));
}

/* ---------- Nav & footer links ---------- */
.nav-link {
  position: relative;
  color: var(--on-surface-variant);
  font-family: Inter, sans-serif;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: color 0.2s ease;
}
.nav-link::after {
  content: '';
  position: absolute;
  left: 0; bottom: -4px;
  width: 0%;
  height: 2px;
  background: var(--primary);
  transition: width 0.25s ease;
}
.nav-link:hover { color: var(--primary); }
.nav-link:hover::after { width: 100%; }

.footer-link {
  color: var(--on-surface-variant);
  cursor: pointer;
  transition: color 0.2s ease, transform 0.2s ease;
  display: inline-block;
}
.footer-link:hover { color: var(--primary); transform: translateX(2px); }

/* ---------- Buttons ---------- */
.btn-shine { position: relative; overflow: hidden; }
.btn-shine::before {
  content: '';
  position: absolute;
  top: 0; left: -75%;
  width: 50%; height: 100%;
  background: linear-gradient(120deg, transparent, rgba(255,255,255,0.35), transparent);
  transform: skewX(-20deg);
  transition: left 0.6s ease;
}
.btn-shine:hover::before { left: 125%; }

/* ---------- Cards & bento hover ---------- */
.bento-card { transition: transform 0.35s ease, box-shadow 0.35s ease; }
.bento-card:hover { transform: translateY(-6px); box-shadow: 0 16px 32px -12px rgba(0, 104, 95, 0.18); }
.bento-card:hover .feature-icon { transform: scale(1.12) rotate(-4deg); }
.feature-icon { transition: transform 0.35s cubic-bezier(0.34, 1.56, 0.64, 1); }

.avatar-ring {
  background: linear-gradient(135deg, var(--primary), var(--primary-container));
  box-shadow: 0 0 0 3px rgba(0, 104, 95, 0.12);
}

/* ---------- Trust bar & benefit micro-interactions ---------- */
.trust-icon { transition: transform 0.3s ease, background-color 0.3s ease; }
.trust-item:hover .trust-icon { transform: scale(1.1); background-color: rgba(0, 104, 95, 0.18); }

.benefit-item, .offer-item {
  opacity: 0;
  transform: translateX(-12px);
  transition: opacity 0.5s ease, transform 0.5s ease;
}
.benefit-item.reveal-in, .offer-item.reveal-in { opacity: 1; transform: translateX(0); }

.star-pop {
  display: inline-block;
  animation: star-pop 0.4s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
@keyframes star-pop {
  0% { opacity: 0; transform: scale(0.4) rotate(-20deg); }
  100% { opacity: 1; transform: scale(1) rotate(0); }
}

/* ---------- Scroll reveal ---------- */
.reveal-up, .trust-item {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal-up.reveal-in, .trust-item.reveal-in { opacity: 1; transform: translateY(0); }

/* ---------- Floating badge bounce ---------- */
@keyframes bounce-slow {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.animate-bounce-slow { animation: bounce-slow 3s ease-in-out infinite; }

/* ---------- Pulse dot ---------- */
@keyframes ping-slow {
  0% { transform: scale(1); opacity: 0.7; }
  75%, 100% { transform: scale(2.2); opacity: 0; }
}
.animate-ping-slow { animation: ping-slow 2s cubic-bezier(0, 0, 0.2, 1) infinite; }

/* ---------- Modals ---------- */
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(20, 27, 43, 0.55);
  backdrop-filter: blur(2px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
  padding: 1rem;
}
.modal-card {
  position: relative;
  background: white;
  border-radius: 1.25rem;
  padding: 2rem;
  max-width: 28rem;
  width: 100%;
  box-shadow: 0 24px 60px -12px rgba(0, 0, 0, 0.25);
}
.modal-card-wide { max-width: 36rem; }

.modal-banner {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
  margin-bottom: 1.75rem;
  padding-right: 2rem;
}
.modal-banner-icon {
  flex-shrink: 0;
  width: 3rem;
  height: 3rem;
  border-radius: 0.9rem;
  background: linear-gradient(135deg, var(--primary), var(--primary-container));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px -6px rgba(0, 104, 95, 0.45);
}

.field-group { position: relative; }
.field-with-icon { position: relative; }
.field-icon {
  position: absolute;
  left: 0.85rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--outline);
  font-size: 20px;
  pointer-events: none;
}
.field-with-icon .field-input { padding-left: 2.6rem; }
.field-with-icon:focus-within .field-icon { color: var(--primary); }

.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.success-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 1.5rem 0.5rem 0.75rem;
}
.success-check {
  width: 4rem;
  height: 4rem;
  border-radius: 9999px;
  background: var(--primary);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  margin-bottom: 1.25rem;
  animation: pop-in 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}
@keyframes pop-in {
  0% { transform: scale(0); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
.modal-close {
  color: var(--on-surface-variant);
  transition: color 0.2s ease, transform 0.2s ease;
}
.modal-close:hover { color: var(--on-surface); transform: rotate(90deg); }

.modal-enter-active, .modal-leave-active { transition: opacity 0.25s ease; }
.modal-enter-from, .modal-leave-to { opacity: 0; }
.modal-enter-active .modal-card, .modal-leave-active .modal-card { transition: transform 0.25s ease, opacity 0.25s ease; }
.modal-enter-from .modal-card, .modal-leave-to .modal-card { transform: scale(0.95); opacity: 0; }

.field-label { display: block; font-size: 14px; font-weight: 500; margin-bottom: 0.5rem; color: var(--on-surface); }
.field-input {
  width: 100%;
  padding: 0.6rem 1rem;
  border: 1px solid var(--outline-variant);
  border-radius: 0.5rem;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}
.field-input:focus {
  outline: none;
  border-color: var(--primary);
  box-shadow: 0 0 0 3px rgba(0, 104, 95, 0.15);
}

.contact-highlight-wrap { padding: 0.5rem; margin: -0.5rem; }
.contact-highlight {
  background: rgba(0, 104, 95, 0.08);
  box-shadow: 0 0 0 2px rgba(0, 104, 95, 0.25);
}

.contact-row {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.5rem;
  border-radius: 0.75rem;
  transition: background 0.2s ease;
}
.contact-row:hover { background: var(--surface-container-low); }
.contact-icon {
  width: 3rem; height: 3rem;
  border-radius: 9999px;
  background: rgba(0, 104, 95, 0.1);
  color: var(--primary);
  display: flex; align-items: center; justify-content: center;
}

/* ---------- Reduced motion ---------- */
@media (prefers-reduced-motion: reduce) {
  .hero-in, .badge-pop, .float-slow, .animate-bounce-slow, .animate-ping-slow,
  .blob, .reveal-up, .trust-item, .benefit-item, .offer-item, .star-pop {
    animation: none !important;
    transition: none !important;
    opacity: 1 !important;
    transform: none !important;
  }
}
</style>

<style>
/* ---------- Icon font (Material Symbols) ----------
   Without this, icon names render as literal text
   like "send_and_archive" instead of glyphs. */
@import url('https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&display=block');

.material-symbols-outlined {
  font-family: 'Material Symbols Outlined';
  font-weight: normal;
  font-style: normal;
  line-height: 1;
  letter-spacing: normal;
  text-transform: none;
  display: inline-block;
  white-space: nowrap;
  word-wrap: normal;
  direction: ltr;
  -webkit-font-smoothing: antialiased;
  font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
}

/* ---------- Design tokens (unchanged from project theme) ---------- */
:root {
  --primary: #00685f;
  --primary-container: #008378;
  --on-primary: #ffffff;
  --on-primary-container: #f4fffc;
  --primary-fixed: #89f5e7;
  --primary-fixed-dim: #6bd8cb;
  --on-primary-fixed: #00201d;
  --on-primary-fixed-variant: #005049;
  --inverse-primary: #6bd8cb;
  --secondary: #5d5f5f;
  --on-secondary: #ffffff;
  --secondary-container: #dfe0e0;
  --on-secondary-container: #616363;
  --secondary-fixed: #e2e2e2;
  --secondary-fixed-dim: #c6c6c7;
  --on-secondary-fixed: #1a1c1c;
  --on-secondary-fixed-variant: #454747;
  --tertiary: #525e5c;
  --on-tertiary: #ffffff;
  --tertiary-container: #6b7775;
  --on-tertiary-container: #f3fffc;
  --tertiary-fixed: #d8e5e2;
  --tertiary-fixed-dim: #bcc9c6;
  --on-tertiary-fixed: #121e1c;
  --on-tertiary-fixed-variant: #3d4947;
  --error: #ba1a1a;
  --on-error: #ffffff;
  --error-container: #ffdad6;
  --on-error-container: #93000a;
  --background: #f9f9ff;
  --on-background: #141b2b;
  --surface: #f9f9ff;
  --on-surface: #141b2b;
  --surface-variant: #dce2f7;
  --on-surface-variant: #3d4947;
  --surface-container: #e9edff;
  --surface-container-low: #f1f3ff;
  --surface-container-high: #e1e8fd;
  --surface-container-highest: #dce2f7;
  --surface-container-lowest: #ffffff;
  --surface-dim: #d3daef;
  --surface-bright: #f9f9ff;
  --surface-tint: #006a61;
  --inverse-surface: #293040;
  --inverse-on-surface: #edf0ff;
  --outline: #6d7a77;
  --outline-variant: #bcc9c6;
  --text-muted: #4B5563;
  --teal-deep: #008080;
  --surface-alt: #F9FAFB;
}

.bg-surface { background-color: var(--surface) !important; }
.bg-surface\/0 { background-color: transparent !important; }
.text-on-surface { color: var(--on-surface) !important; }
.bg-primary { background-color: var(--primary) !important; }
.text-primary { color: var(--primary) !important; }
.bg-primary-container { background-color: var(--primary-container) !important; }
.text-on-primary { color: var(--on-primary) !important; }
.bg-surface-container-low { background-color: var(--surface-container-low) !important; }
.text-on-surface-variant { color: var(--on-surface-variant) !important; }
.bg-surface-container-highest { background-color: var(--surface-container-highest) !important; }
.text-text-muted { color: var(--text-muted) !important; }
.border-outline-variant { border-color: var(--outline-variant) !important; }
.bg-primary\/10 { background-color: rgba(0, 104, 95, 0.1) !important; }
.text-primary\/20 { color: rgba(0, 104, 95, 0.2) !important; }
.bg-primary\/5 { background-color: rgba(0, 104, 95, 0.05) !important; }
.shadow-primary\/20 { box-shadow: 0 10px 25px -5px rgba(0, 104, 95, 0.2) !important; }
.border-primary\/10 { border-color: rgba(0, 104, 95, 0.1) !important; }
.bg-white\/50 { background-color: rgba(255, 255, 255, 0.5) !important; }
.bg-white\/10 { background-color: rgba(255, 255, 255, 0.1) !important; }
.border-white\/30 { border-color: rgba(255, 255, 255, 0.3) !important; }
.border-white\/40 { border-color: rgba(255, 255, 255, 0.4) !important; }
.bg-surface\/90 { background-color: rgba(249, 249, 255, 0.9) !important; }

.text-blue-600, .text-blue-500, .text-blue-400, .text-blue-300, .text-blue-700, .text-blue-800,
.text-blue-900, .text-blue-950 { color: var(--primary) !important; }
.bg-blue-600, .bg-blue-500, .bg-blue-400, .bg-blue-300, .bg-blue-700, .bg-blue-800,
.bg-blue-900, .bg-blue-950 { background-color: var(--primary) !important; }
.border-blue-600, .border-blue-500, .border-blue-400, .border-blue-300, .border-blue-700, .border-blue-800,
.border-blue-900, .border-blue-950 { border-color: var(--primary) !important; }
</style>