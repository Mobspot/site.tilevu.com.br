// Progressive enhancement: content remains visible without JavaScript.
if (!matchMedia('(prefers-reduced-motion: reduce)').matches && 'IntersectionObserver' in window) {
  const observer = new IntersectionObserver(entries => {
    for (const entry of entries) if (entry.isIntersecting) {
      entry.target.animate([{transform:'translateY(14px)',opacity:.65},{transform:'translateY(0)',opacity:1}], {duration:500,easing:'ease-out'});
      observer.unobserve(entry.target);
    }
  }, {threshold:.12});
  document.querySelectorAll('.reveal').forEach(element => observer.observe(element));
}
